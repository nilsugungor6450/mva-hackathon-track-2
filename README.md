# MVA Hackathon 2026 – Track 2: Drug Repurposing

**Participant:** nilsu6450 (individual)
**Track 1 repository (variant prediction):** https://github.com/nilsugungor6450/mva-hackathon

> All drug candidates in this repository are hypotheses for follow-up experiments.
> They are not treatment recommendations and no doses are proposed.

## Summary

Track 1 identified a compound heterozygous pair in **BUB1B**, the gene for mosaic variegated
aneuploidy type 1 (MVA1):

| Variant | Effect |
|---|---|
| p.Leu737Ter | Early stop codon → expected nonsense-mediated decay → **null allele** |
| p.Asn1002Lys | Missense in the folded C-terminal domain → **hypomorphic allele** |

**Mechanism:** partial loss of function. Too little BUBR1 protein (the product of BUB1B) weakens the
spindle assembly checkpoint, which causes mosaic aneuploidy, cellular stress and senescence, growth
restriction and cancer predisposition.

**Key evidence:** Open Targets shows no approved or clinical drug for BUB1B, so all candidates act
indirectly. AlphaFold places N1002 inside a compact, confidently predicted domain (pLDDT 91.1), which
suggests the missense change may destabilise the remaining protein.

**Candidates (7, in three tiers):**

| Tier | Candidates |
|---|---|
| 1. Restore BUBR1 | **NAD+ precursors (lead)** · chemical chaperone (sodium phenylbutyrate, ursodiol) · combination of both |
| 2. Protect the cells | dasatinib (senolytic) · low-dose sirolimus · N-acetylcysteine |
| 3. Exploratory | metformin or hydroxychloroquine |

## Where to find what

| I want to… | Go to |
|---|---|
| Read the full report | [`track2/nilsu6450_track2_report.pdf`](track2/nilsu6450_track2_report.pdf) |
| See the candidate grading table | [`track2/candidates.csv`](track2/candidates.csv) |
| Reproduce the database evidence | [`track2/evidence_check.py`](track2/evidence_check.py) (instructions in [`track2/README.md`](track2/README.md)) |
| See the script output | [`results/track2_evidence.txt`](results/track2_evidence.txt) |
| Read the methods description (Tracks 1 and 2) | [`docs/nilsu6450_methods_description_form.xlsx`](docs/nilsu6450_methods_description_form.xlsx) |

## Repository layout

```
.
├── README.md                      this file
├── track2/
│   ├── nilsu6450_track2_report.pdf   full report
│   ├── candidates.csv                7 candidates with evidence grading
│   ├── evidence_check.py             reproduces Open Targets + AlphaFold evidence
│   └── README.md                     how to run the script
├── results/
│   └── track2_evidence.txt           output of evidence_check.py
└── docs/
    └── nilsu6450_methods_description_form.xlsx
```

## Reproduce

```bash
python3 track2/evidence_check.py
```

Python 3.9+ and internet access. No packages to install. Runs in under a minute.

## Data

No patient data is stored in this repository. The analysis uses only public resources
(Open Targets, AlphaFold DB, UniProt, PubMed literature) together with the Track 1 variant calls.

## Use of AI assistance

Anthropic claude.ai, Claude Opus 5.5, Claude Pro plan (consumer terms), "Help improve Claude"
model-training setting turned off. Used for literature search support, explaining biological
concepts, structuring the reasoning, drafting the report and writing the evidence script. All
candidates and claims were reviewed by me.
