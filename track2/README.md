# Track 2 – Drug Repurposing

Report: `nilsu6450_track2_report.pdf` (in this folder).

## How the candidates were found

1. **Mechanism** from the Track 1 variants in BUB1B (p.Leu737Ter null + p.Asn1002Lys hypomorphic):
   partial loss of function of BUBR1 → weak spindle assembly checkpoint → mosaic aneuploidy.
2. **Database check** (Open Targets, AlphaFold): no approved or clinical drug acts on BUB1B, and
   N1002 lies in a compact, confidently predicted C-terminal domain.
3. **Literature curation** of approved drugs that act on each step of the mechanism, graded with the
   same criteria for every candidate.

## Files

| File | What it is |
|---|---|
| `evidence_check.py` | Reproduces the database evidence (Open Targets associations and tractability; AlphaFold pLDDT and PAE). Standard library only. |
| `candidates.csv` | The 7 candidates with strategy, evidence level, paediatric use, risks and overall grade (Table 2 of the report). |

## Run

```bash
python track2/evidence_check.py
```

Output is printed and saved to `results/track2_evidence.txt`.
