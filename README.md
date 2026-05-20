# SSVEP TMSi Overt Pilot

This repository contains the cleaned experiment code, sanitized analysis outputs, and reproducibility utilities for a single-subject overt SSVEP pilot recorded with a TMSi EEG system.

Raw EEG recordings, converted EEG files, videos, and audio files are intentionally not stored in this repository.

## Repository structure

- `experiment/`  
  PsychoPy experiment code used for the overt SSVEP pilot.

- `scripts/`  
  Lightweight analysis and validation scripts that can run on sanitized outputs.

- `results/step06_enhanced_preprocessing_spectral/`  
  Enhanced preprocessing outputs, exact-frequency SSVEP metrics, spectral plots, and topographic figures.

- `results/step07_statistical_validation/`  
  Statistical validation tables and report addenda derived from sanitized Step 06 outputs.

## Data policy

This repository should not contain raw or heavy research data.

Do not commit raw EEG recordings, converted EEG files, video files, audio files, local project folders, or machine-specific paths.

Only commit lightweight and shareable material such as source code, sanitized summary tables, result figures, Markdown reports, LaTeX source, and privacy-checked PDFs.

## Validated pilot results

The current analysis supports reliable SSVEP responses in this pilot recording.

Key results:

- Trigger structure was successfully recovered from the decoded trigger channel.
- CCA classification accuracy was 37 out of 40 trials, equal to 92.5%.
- The 9 Hz condition was classified at 100%.
- The 14 Hz condition was classified at 85%.
- Enhanced exact-frequency analysis showed target-specific posterior responses at the fundamental and harmonic frequencies.
- Trial-level selectivity was positive in most usable trials.

## Reproducibility

The raw EEG recording is intentionally excluded. To reproduce the full analysis locally, provide paths to the local TMSi Python Interface checkout, the local raw EEG recording, and the local project or analysis directory.

Use command-line arguments or local environment variables rather than hard-coded private paths.

The statistical validation script can be run directly from the repository root because it uses only sanitized CSV outputs already stored in `results/`.

Command:

    python scripts/07_statistical_validation_from_step06.py

## Notes

This is a pilot and single-subject analysis package. The results are suitable for internal reporting, method validation, and supervisor handoff. Generalized claims require additional participants and repeated recordings.
