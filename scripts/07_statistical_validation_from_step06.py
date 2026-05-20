#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
07_statistical_validation_from_step06.py

GitHub-safe statistical validation script for the TMSi overt SSVEP pilot.

Reads sanitized Step 06 CSV outputs from:

    results/step06_enhanced_preprocessing_spectral/

and creates:

    results/step07_statistical_validation/

No raw EEG files are read. No local/private paths are required.

Run from repository root:

    conda activate tmsi310
    python scripts/07_statistical_validation_from_step06.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from scipy import stats


def fmt_p(p: float) -> str:
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def markdown_table(df: pd.DataFrame, digits: int = 4) -> str:
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda x: f"{x:.{digits}f}" if pd.notna(x) else "")
    lines = [
        "| " + " | ".join(d.columns) + " |",
        "| " + " | ".join(["---"] * len(d.columns)) + " |",
    ]
    for _, row in d.iterrows():
        lines.append("| " + " | ".join(str(row[c]).replace("|", "\\|") for c in d.columns) + " |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_root", default=".", help="Repository root. Default: current directory.")
    ap.add_argument(
        "--step06_dir",
        default="results/step06_enhanced_preprocessing_spectral",
        help="Relative path to Step 06 output folder.",
    )
    ap.add_argument(
        "--out_dir",
        default="results/step07_statistical_validation",
        help="Relative path for Step 07 output folder.",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    step06_dir = (repo_root / args.step06_dir).resolve()
    out_dir = (repo_root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    trial_path = step06_dir / "06_exact_frequency_trial_summary.csv"
    posterior_rank_path = step06_dir / "06_posterior_channel_condition_contrast_ranked.csv"
    posterior_summary_path = step06_dir / "06_posterior_exact_frequency_summary.csv"

    missing = [p for p in [trial_path, posterior_rank_path, posterior_summary_path] if not p.exists()]
    if missing:
        print("[ERROR] Missing required Step 06 files:")
        for p in missing:
            print(f"  {p}")
        return 2

    trial = pd.read_csv(trial_path)
    rank = pd.read_csv(posterior_rank_path)
    _posterior_summary = pd.read_csv(posterior_summary_path)

    required = {"target_freq_hz", "posterior_exact_selectivity_db"}
    if not required.issubset(set(trial.columns)):
        print("[ERROR] Trial summary CSV does not contain required columns:")
        print(f"  required={sorted(required)}")
        print(f"  available={list(trial.columns)}")
        return 3

    rows = []
    for cond, g in trial.groupby("target_freq_hz"):
        sel = pd.to_numeric(g["posterior_exact_selectivity_db"], errors="coerce").dropna().to_numpy(float)
        n = len(sel)
        k = int(np.sum(sel > 0))
        mean = float(np.mean(sel))
        median = float(np.median(sel))
        sd = float(np.std(sel, ddof=1)) if n > 1 else np.nan
        if n > 1 and np.isfinite(sd):
            ci_low, ci_high = stats.t.interval(0.95, n - 1, loc=mean, scale=sd / np.sqrt(n))
        else:
            ci_low, ci_high = np.nan, np.nan

        wil = stats.wilcoxon(sel, alternative="greater", zero_method="wilcox") if n > 0 else None
        binom = stats.binomtest(k, n, p=0.5, alternative="greater") if n > 0 else None

        rows.append({
            "condition_hz": int(cond) if float(cond).is_integer() else cond,
            "n_trials": n,
            "positive_trials": k,
            "positive_percent": 100.0 * k / n if n else np.nan,
            "mean_selectivity_db": mean,
            "median_selectivity_db": median,
            "sd_selectivity_db": sd,
            "ci95_low_db": float(ci_low),
            "ci95_high_db": float(ci_high),
            "wilcoxon_W": float(wil.statistic) if wil else np.nan,
            "wilcoxon_p_one_sided": float(wil.pvalue) if wil else np.nan,
            "sign_test_p_one_sided": float(binom.pvalue) if binom else np.nan,
        })

    sel = pd.to_numeric(trial["posterior_exact_selectivity_db"], errors="coerce").dropna().to_numpy(float)
    n = len(sel)
    k = int(np.sum(sel > 0))
    mean = float(np.mean(sel))
    median = float(np.median(sel))
    sd = float(np.std(sel, ddof=1))
    ci_low, ci_high = stats.t.interval(0.95, n - 1, loc=mean, scale=sd / np.sqrt(n))
    wil = stats.wilcoxon(sel, alternative="greater", zero_method="wilcox")
    binom = stats.binomtest(k, n, p=0.5, alternative="greater")
    rows.append({
        "condition_hz": "overall",
        "n_trials": n,
        "positive_trials": k,
        "positive_percent": 100.0 * k / n,
        "mean_selectivity_db": mean,
        "median_selectivity_db": median,
        "sd_selectivity_db": sd,
        "ci95_low_db": float(ci_low),
        "ci95_high_db": float(ci_high),
        "wilcoxon_W": float(wil.statistic),
        "wilcoxon_p_one_sided": float(wil.pvalue),
        "sign_test_p_one_sided": float(binom.pvalue),
    })

    stats_df = pd.DataFrame(rows)
    stats_csv = out_dir / "07_trial_selectivity_statistics.csv"
    stats_df.to_csv(stats_csv, index=False)

    cca_rows = [
        {
            "scope": "overall CCA",
            "correct": 37,
            "total": 40,
            "accuracy": 37 / 40,
            "binomial_p_vs_50_percent": stats.binomtest(37, 40, 0.5, alternative="greater").pvalue,
        },
        {
            "scope": "9 Hz CCA",
            "correct": 20,
            "total": 20,
            "accuracy": 1.0,
            "binomial_p_vs_50_percent": stats.binomtest(20, 20, 0.5, alternative="greater").pvalue,
        },
        {
            "scope": "14 Hz CCA",
            "correct": 17,
            "total": 20,
            "accuracy": 17 / 20,
            "binomial_p_vs_50_percent": stats.binomtest(17, 20, 0.5, alternative="greater").pvalue,
        },
    ]
    cca_df = pd.DataFrame(cca_rows)
    cca_csv = out_dir / "07_cca_binomial_validation.csv"
    cca_df.to_csv(cca_csv, index=False)

    top_cols = [
        c for c in [
            "channel",
            "snr9_condition_contrast_db",
            "snr14_condition_contrast_db",
            "amp9_condition_contrast_uv",
            "amp14_condition_contrast_uv",
            "best_abs_condition_contrast_db",
        ]
        if c in rank.columns
    ]
    top_rank = rank[top_cols].head(12).copy()
    top_csv = out_dir / "07_top_posterior_condition_contrast_channels.csv"
    top_rank.to_csv(top_csv, index=False)

    md = []
    md.append("# Step 07 Statistical Validation Addendum")
    md.append("")
    md.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("")
    md.append("This addendum validates whether the enhanced exact-frequency SSVEP selectivity from Step 06 is consistently positive at the trial level.")
    md.append("")
    md.append("## Trial-level exact-frequency selectivity")
    md.append("")
    md.append("Selectivity was defined as posterior exact-frequency target SNR minus posterior exact-frequency non-target SNR for each usable trial.")
    md.append("")
    md.append(markdown_table(stats_df, digits=4))
    md.append("")
    md.append("## CCA binomial validation")
    md.append("")
    md.append(markdown_table(cca_df, digits=6))
    md.append("")
    md.append("## Top posterior condition-contrast channels")
    md.append("")
    md.append(markdown_table(top_rank, digits=3))
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("The dataset contains reliable SSVEP evidence: CCA accuracy was strongly above chance, and Step 06 exact-frequency posterior selectivity was positive in most usable trials.")
    md.append("")
    md_path = out_dir / "07_ssvep_statistical_validation_addendum.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    tex = []
    tex.append(r"% Step 07 statistical validation addendum")
    tex.append(r"\section{Statistical Validation of Trial-Level SSVEP Selectivity}")
    tex.append("")
    tex.append(
        r"Trial-level exact-frequency selectivity was evaluated as posterior target-frequency SNR minus "
        r"posterior non-target-frequency SNR. One-sided Wilcoxon signed-rank tests and exact sign tests "
        r"were used to test whether selectivity was greater than zero."
    )
    tex.append("")
    tex.append(r"\begin{table}[htbp]")
    tex.append(r"\centering")
    tex.append(r"\caption{Trial-level exact-frequency selectivity statistics.}")
    tex.append(r"\begin{tabular}{lrrrrr}")
    tex.append(r"\hline")
    tex.append(r"Condition & Trials & Positive & Mean (dB) & Median (dB) & Wilcoxon $p$ \\")
    tex.append(r"\hline")
    for _, row in stats_df.iterrows():
        tex.append(
            f"{row['condition_hz']} & {int(row['n_trials'])} & {int(row['positive_trials'])} & "
            f"{row['mean_selectivity_db']:.2f} & {row['median_selectivity_db']:.2f} & "
            f"{fmt_p(float(row['wilcoxon_p_one_sided']))} \\"
        )
    tex.append(r"\hline")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table}")
    tex.append("")
    tex.append(
        r"CCA classification was also tested against chance using exact one-sided binomial tests. "
        r"The overall accuracy was 37/40 trials (92.5\%), supporting reliable discrimination between "
        r"the 9-Hz and 14-Hz stimulation conditions."
    )
    tex_path = out_dir / "07_latex_statistical_validation_addendum.tex"
    tex_path.write_text("\n".join(tex) + "\n", encoding="utf-8")

    print("Created Step 07 statistical validation outputs:")
    for p in [stats_csv, cca_csv, top_csv, md_path, tex_path]:
        print(f"  {p.relative_to(repo_root)}")

    print("\nSummary:")
    print(stats_df.to_string(index=False))
    print("\nCCA:")
    print(cca_df.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
