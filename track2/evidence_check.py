"""Track 2 evidence check: reproduces the database evidence used in the report.

What it does
  1. Open Targets (GraphQL API): BUB1B disease associations, the evidence types
     behind the MVA association (including whether any drug/clinical evidence
     exists), and the tractability assessment.
  2. AlphaFold DB: downloads the BUB1B model (AF-O60566-F1) and its predicted
     aligned error (PAE), then reports the model confidence (pLDDT) at residue
     1002 and the mean PAE inside the C-terminal block (residues 720-1050)
     compared with the rest of the protein.

Usage
  python track2/evidence_check.py

Requirements
  Python 3.9+ and internet access. Standard library only, no packages needed.
  Output is printed and also saved to results/track2_evidence.txt.
"""
import json
import urllib.request
from pathlib import Path

GENE_ENSEMBL = "ENSG00000156970"   # BUB1B
UNIPROT = "O60566"                 # BUBR1
VARIANT_RESIDUE = 1002             # p.Asn1002Lys
DOMAIN = (720, 1050)               # C-terminal kinase-like block seen in the PAE map

OT_URL = "https://api.platform.opentargets.org/api/v4/graphql"
AF_API = f"https://alphafold.ebi.ac.uk/api/prediction/{UNIPROT}"

lines = []


def out(text=""):
    print(text)
    lines.append(text)


def get_json(url, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get_text(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read().decode()


# ---------------------------------------------------------------- Open Targets
def open_targets():
    query = """
    query ($id: String!) {
      target(ensemblId: $id) {
        approvedSymbol
        tractability { modality label value }
        associatedDiseases(page: {index: 0, size: 10}) {
          rows { disease { id name } score datatypeScores { id score } }
        }
      }
    }"""
    t = get_json(OT_URL, {"query": query, "variables": {"id": GENE_ENSEMBL}})["data"]["target"]
    out(f"== Open Targets: {t['approvedSymbol']} ({GENE_ENSEMBL})")

    out("\n-- Top disease associations and their evidence types")
    for row in t["associatedDiseases"]["rows"]:
        types = ", ".join(f"{d['id']}={d['score']:.2f}" for d in row["datatypeScores"])
        out(f"{row['disease']['name']} [{row['disease']['id']}]  score={row['score']:.2f}")
        out(f"    evidence: {types}")
        if "variegated" in row["disease"]["name"].lower():
            drug_types = [d for d in row["datatypeScores"] if d["id"] in ("known_drug", "clinical")]
            out("    -> drug / clinical evidence for this MVA association: "
                + ("YES " + str(drug_types) if drug_types else "NONE"))

    out("\n-- Tractability (only items marked TRUE)")
    true_items = [x for x in t["tractability"] if x["value"]]
    for x in true_items:
        out(f"    {x['modality']}: {x['label']}")
    approved = [x for x in true_items if "approved" in x["label"].lower() or "clinical" in x["label"].lower()]
    out("    -> approved / clinical-stage drug in any modality: " + ("YES" if approved else "NONE"))


# ------------------------------------------------------------------ AlphaFold
def alphafold():
    entry = get_json(AF_API)[0]
    out(f"\n== AlphaFold: {entry['entryId']} (model version {entry.get('latestVersion', '?')})")

    # pLDDT is stored in the B-factor column of the PDB file (one value per residue, CA atom)
    plddt = {}
    for line in get_text(entry["pdbUrl"]).splitlines():
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            plddt[int(line[22:26])] = float(line[60:66])
    mean_plddt = sum(plddt.values()) / len(plddt)
    out(f"mean pLDDT (whole protein): {mean_plddt:.1f}")
    out(f"pLDDT at residue {VARIANT_RESIDUE}: {plddt[VARIANT_RESIDUE]:.1f}"
        "   (>90 very high, 70-90 high, 50-70 low, <50 very low)")
    lo, hi = DOMAIN
    dom = [v for k, v in plddt.items() if lo <= k <= hi]
    out(f"mean pLDDT in residues {lo}-{hi}: {sum(dom) / len(dom):.1f}")

    # PAE: matrix of expected position errors (Angstrom); low values = rigid, well-defined block
    pae_doc = get_json(entry["paeDocUrl"])
    pae = (pae_doc[0] if isinstance(pae_doc, list) else pae_doc)["predicted_aligned_error"]
    n = len(pae)
    inside = [pae[i][j] for i in range(lo - 1, hi) for j in range(lo - 1, hi)]
    outside = [pae[i][j] for i in range(n) for j in range(n)
               if not (lo - 1 <= i < hi and lo - 1 <= j < hi)]
    out(f"mean PAE inside residues {lo}-{hi}: {sum(inside) / len(inside):.1f} A")
    out(f"mean PAE elsewhere:              {sum(outside) / len(outside):.1f} A")
    out(f"-> residue {VARIANT_RESIDUE} lies inside the {lo}-{hi} block: {lo <= VARIANT_RESIDUE <= hi}")


if __name__ == "__main__":
    open_targets()
    alphafold()
    results = Path(__file__).resolve().parents[1] / "results"
    results.mkdir(exist_ok=True)
    (results / "track2_evidence.txt").write_text("\n".join(lines) + "\n")
    print(f"\nSaved to {results / 'track2_evidence.txt'}")
