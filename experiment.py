"""Decision curve analysis for selective dry-cow therapy.

From the Singularity v3 forecast T3v3-2026-0017 (decision curve analysis -> Animal Science and Zoology).
A test-guided dry-off strategy (antibiotic only for cows the test flags, internal teat sealant for all) is compared
with blanket antibiotic therapy and with no antibiotics, by net benefit across threshold probabilities.

Net benefit of treating by a rule, per cow:  NB = TP/N - FP/N * pt/(1 - pt),
where pt is the threshold probability: the probability of infection at which a farmer or vet is indifferent between
treating and not treating (pt/(1-pt) = harm of an unnecessary antibiotic tube / benefit of treating an infected cow).

All scenario values are illustrative and stated in the paper; the closed-form results do not depend on them.
Run: python experiment.py -> results.json, fig_dca.png, fig_regions.png, fig_uncertainty.png
"""

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261105)
PT = np.linspace(0.01, 0.60, 237)
TESTS = {"algorithm (SCC + mastitis history)": (0.80, 0.55), "on-farm culture": (0.85, 0.75)}
PREV = 0.30


def nb_all(prev, pt):
    return prev - (1 - prev) * pt / (1 - pt)


def nb_test(prev, se, sp, pt):
    return se * prev - (1 - sp) * (1 - prev) * pt / (1 - pt)


def useful_interval(prev, se, sp):
    """Threshold odds w = pt/(1-pt) for which the test beats both blanket therapy and no antibiotics."""
    lo = (1 - se) * prev / (sp * (1 - prev))
    hi = se * prev / ((1 - sp) * (1 - prev)) if sp < 1 else np.inf
    to_p = lambda w: w / (1 + w)
    return to_p(lo), to_p(hi)


def main():
    res = {"scenario": {"prevalence": PREV, "tests": TESTS}, "intervals": {}, "grid": {}, "uncertainty": {}}
    for name, (se, sp) in TESTS.items():
        res["intervals"][name] = {str(p): useful_interval(p, se, sp) for p in (0.1, 0.2, 0.3, 0.4, 0.5)}
    # Monte Carlo over parameter uncertainty: herd prevalence and test accuracy are not known exactly
    n = 20000
    prev = RNG.uniform(0.15, 0.45, n)
    for name, (se, sp) in TESTS.items():
        a = 60
        S = RNG.beta(se * a, (1 - se) * a, n)
        P = RNG.beta(sp * a, (1 - sp) * a, n)
        best = []
        for pt in PT:
            t, al = nb_test(prev, S, P, pt), nb_all(prev, pt)
            best.append(float(np.mean((t > al) & (t > 0))))
        res["uncertainty"][name] = best
    res["pt"] = PT.tolist()
    (HERE / "results.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    figures(res)
    for name in TESTS:
        print(name, {k: [round(x, 3) for x in v] for k, v in res["intervals"][name].items()})


def figures(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(PT, nb_all(PREV, PT), label="blanket antibiotic", lw=2, color="0.3")
    ax.plot(PT, 0 * PT, label="no antibiotic (sealant only)", lw=2, color="0.6", ls="--")
    for (name, (se, sp)), c in zip(TESTS.items(), ["#1f77b4", "#d62728"]):
        ax.plot(PT, nb_test(PREV, se, sp, PT), label=f"{name}: Se {se:.2f}, Sp {sp:.2f}", lw=2, color=c)
    ax.set_ylim(-0.08, PREV + 0.02)
    ax.set_xlabel("threshold probability of infection, $p_t$")
    ax.set_ylabel("net benefit (infected cows treated, per cow)")
    ax.set_title(f"Decision curves, herd prevalence {PREV:.0%}", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HERE / "fig_dca.png", dpi=160)

    fig, axs = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    prevs = np.linspace(0.05, 0.7, 200)
    for ax, (name, (se, sp)) in zip(axs, TESTS.items()):
        Pg, Tg = np.meshgrid(prevs, PT)
        t, al = nb_test(Pg, se, sp, Tg), nb_all(Pg, Tg)
        best = np.where((t > al) & (t > 0), 2, np.where(al > 0, 1, 0))
        ax.contourf(Pg, Tg, best, levels=[-0.5, 0.5, 1.5, 2.5], colors=["#eeeeee", "#bbbbbb", "#7fb3e6"])
        ax.set_title(f"{name}\n(Se {se:.2f}, Sp {sp:.2f})", fontsize=10)
        ax.set_xlabel("herd prevalence of infection at dry-off")
    axs[0].set_ylabel("threshold probability $p_t$")
    for ax in axs:
        ax.text(0.08, 0.57, "no antibiotic best", fontsize=9, va="top")
        ax.text(0.68, 0.03, "blanket antibiotic best", fontsize=9, ha="right", va="bottom")
        ax.text(0.45, 0.30, "test-guided best", fontsize=10, ha="center", color="#0b3d6b", weight="bold")
    fig.tight_layout()
    fig.savefig(HERE / "fig_regions.png", dpi=160)

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for (name, v), c in zip(res["uncertainty"].items(), ["#1f77b4", "#d62728"]):
        ax.plot(PT, v, label=name, lw=2, color=c)
    ax.set_xlabel("threshold probability $p_t$")
    ax.set_ylabel("probability the test-guided rule is best")
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "fig_uncertainty.png", dpi=160)


if __name__ == "__main__":
    main()
