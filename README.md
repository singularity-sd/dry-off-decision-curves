# When does a test pay off at dry-off? Decision curve analysis for selective dry-cow therapy

Decision curve analysis for selective dry-cow therapy, from a Singularity v3 forecast.

**Paper:** [paper.pdf](paper.pdf) · **Page:** [singularitysd.com/research/dry-off.html](https://singularitysd.com/research/dry-off.html) · Preprint, not yet peer reviewed.

## Abstract

Selective dry-cow therapy gives antibiotics at dry-off only to cows that a test flags as infected, and an internal teat sealant to all. Evaluations so far use sensitivity and specificity, or partial budgets in currency. Neither answers the question a veterinarian faces: *for my herd and my view of the trade-off between antibiotic use and missed infections, is the test better than treating every cow, or none?* Decision curve analysis, standard for diagnostic decisions in human medicine, answers exactly this through the net benefit across threshold probabilities. We give the closed-form conditions under which a test-guided rule beats blanket therapy and no antibiotics: with herd prevalence $\pi$, sensitivity $Se$, specificity $Sp$ and threshold odds $w=p_t/(1-p_t)$, the test is best if and only if \[ \frac{(1-Se) \pi}{Sp (1-\pi)} < w < \frac{Se \pi}{(1-Sp)(1-\pi)}. \] In an illustrative herd with 30% prevalence, an algorithm with $Se=0.80$, $Sp=0.55$ is best for thresholds between 13.5% and 43%, and an on-farm culture with $Se=0.85$, $Sp=0.75$ for thresholds between 8% and 59%. Below these ranges blanket therapy wins; above them, no antibiotics. Under parameter uncertainty the culture-guided rule is best with probability above 0.8 for thresholds between 11.5% and 47%. The analysis turns stewardship priorities into a single number a herd can reason about, and shows when a cheap algorithm is enough.

## How it was made

This study started from the Singularity forecast **T3v3-2026-0017**: a method predicted to enter a new field. It was then tested once, with the plan fixed before looking at the results.

## What is in this repository

| file | what it is |
|---|---|
| `experiment.py` | reproduces the study end to end |
| `fig_dca.png` | figure |
| `fig_regions.png` | figure |
| `fig_uncertainty.png` | figure |
| `main.tex` | LaTeX source of the paper |
| `paper.pdf` | the paper |
| `results.json` | every number reported in the paper |

## Reproduce

```bash
pip install matplotlib numpy
python experiment.py
```

It writes `results.json` and the figures next to the script.

## Cite

```bibtex
@misc{singularity_dry_off_decision_curves_2026,
  title  = {When does a test pay off at dry-off? Decision curve analysis for selective dry-cow therapy},
  author = {Singularity},
  year   = {2026},
  url    = {https://github.com/singularity-sd/dry-off-decision-curves}
}
```

## License

Code: MIT (`LICENSE`). Paper, text and figures: CC BY 4.0 (`LICENSE-paper.md`). Third-party data keep their own licence where stated.

---

Part of [Singularity](https://singularitysd.com): forecasting where science goes next, then testing it.
