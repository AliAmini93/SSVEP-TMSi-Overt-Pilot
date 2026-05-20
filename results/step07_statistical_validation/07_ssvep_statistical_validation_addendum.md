# Step 07 Statistical Validation Addendum

Generated: 2026-05-20 16:55:25

This addendum validates whether the enhanced exact-frequency SSVEP selectivity from Step 06 is consistently positive at the trial level.

## Trial-level exact-frequency selectivity

Selectivity was defined as posterior exact-frequency target SNR minus posterior exact-frequency non-target SNR for each usable trial.

| condition_hz | n_trials | positive_trials | positive_percent | mean_selectivity_db | median_selectivity_db | sd_selectivity_db | ci95_low_db | ci95_high_db | wilcoxon_W | wilcoxon_p_one_sided | sign_test_p_one_sided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9 | 19 | 18 | 94.7368 | 5.8247 | 6.5020 | 3.9187 | 3.9360 | 7.7135 | 186.0000 | 0.0000 | 0.0000 |
| 14 | 20 | 16 | 80.0000 | 4.6444 | 5.2868 | 4.7242 | 2.4334 | 6.8554 | 192.0000 | 0.0002 | 0.0059 |
| overall | 39 | 34 | 87.1795 | 5.2194 | 5.9346 | 4.3348 | 3.8143 | 6.6246 | 740.0000 | 0.0000 | 0.0000 |

## CCA binomial validation

| scope | correct | total | accuracy | binomial_p_vs_50_percent |
| --- | --- | --- | --- | --- |
| overall CCA | 37 | 40 | 0.925000 | 0.000000 |
| 9 Hz CCA | 20 | 20 | 1.000000 | 0.000001 |
| 14 Hz CCA | 17 | 20 | 0.850000 | 0.001288 |

## Top posterior condition-contrast channels

| channel | snr9_condition_contrast_db | snr14_condition_contrast_db | amp9_condition_contrast_uv | amp14_condition_contrast_uv | best_abs_condition_contrast_db |
| --- | --- | --- | --- | --- | --- |
| Oz | 15.303 | 7.974 | 0.620 | 0.282 | 15.303 |
| O1 | 13.531 | 9.198 | 0.557 | 0.278 | 13.531 |
| PO3 | 6.389 | 9.043 | 0.243 | 0.161 | 9.043 |
| O2 | 8.217 | 7.592 | 0.303 | 0.226 | 8.217 |
| PO7 | 6.323 | 8.034 | 0.247 | 0.156 | 8.034 |
| POz | 7.183 | 7.970 | 0.217 | 0.131 | 7.970 |
| PO4 | 4.571 | 5.646 | 0.160 | 0.104 | 5.646 |
| PO8 | 4.992 | 3.400 | 0.162 | 0.087 | 4.992 |
| P5 | 4.254 | 2.229 | 0.118 | 0.014 | 4.254 |
| P3 | 4.026 | 1.045 | 0.074 | 0.016 | 4.026 |
| P7 | 3.801 | 2.110 | 0.137 | 0.030 | 3.801 |
| Pz | 1.513 | 0.673 | 0.022 | 0.026 | 1.513 |

## Interpretation

The dataset contains reliable SSVEP evidence: CCA accuracy was strongly above chance, and Step 06 exact-frequency posterior selectivity was positive in most usable trials.
