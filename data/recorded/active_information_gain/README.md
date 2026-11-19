# Active information-gain baseline artifacts

- `main/`: adopted strict-paired run and aggregate results. All 1,216 rows reuse the
  exact first question and first Target response from the corresponding
  `dialogue_only` row.
- Debug-only runs `active_information_gain_paired_smoke`,
  `active_information_gain_smoke`, and
  `active_information_gain_unpaired_batch_diagnostic_20260913` were deleted on
  2026-09-15.
- The deleted unpaired diagnostic completed 1,216 rows, but 488 first Target
  responses drifted from the existing paired run because they were sampled in a
  separate vLLM batch. It must not be used for reported statistics.

The adopted report is `main/aggregate/report.md`; the implementation and protocol
boundary are documented in `docs/access_active_information_gain_baseline.md`.
