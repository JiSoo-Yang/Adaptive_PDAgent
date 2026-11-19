# IEEE Access reviewer experiment audit

## Primary Adaptive PD-Agent versus Original PD-Agent result

The per-instance test value is the equal-weight mean of four majority-normalized dimension gains. All 304 persona instances are paired.

| Target | Paired Δ Average Gain | 95% CI | p | BH p | + / − / tie |
|---|---:|---:|---:|---:|---:|
| Qwen/Qwen3-1.7B | +0.0190 | [-0.0139, +0.0519] | 0.2112 | 0.2112 | 63 / 54 / 187 |
| Qwen/Qwen3-4B | +0.0397 | [+0.0046, +0.0753] | 0.02235 | 0.03007 | 80 / 53 / 171 |
| meta-llama/Llama-3.2-3B-Instruct | +0.0536 | [+0.0181, +0.0901] | 0.001188 | 0.00475 | 98 / 63 / 143 |
| google/gemma-3-4b-it | +0.0281 | [-0.0088, +0.0656] | 0.02255 | 0.03007 | 81 / 72 / 151 |

The primary Benjamini–Hochberg family is `adaptive_vs_original_macro_gain_across_4_targets`. It contains the four target-level Average Gain contrasts. The 16 dimension contrasts form the separate `adaptive_vs_original_4_dimensions_across_4_targets` family.

## Protocol checks

- Qwen/Qwen3-1.7B: 304 paired personas; same persona=True; same first question=True; same first answer=True; adaptive early stops=0.
- Qwen/Qwen3-4B: 304 paired personas; same persona=True; same first question=True; same first answer=True; adaptive early stops=0.
- meta-llama/Llama-3.2-3B-Instruct: 304 paired personas; same persona=True; same first question=True; same first answer=True; adaptive early stops=0.
- google/gemma-3-4b-it: 304 paired personas; same persona=True; same first question=True; same first answer=True; adaptive early stops=0.

## Interpretation boundary

The existing final prediction is deterministic and has one execution per persona-method pair. These paired tests quantify sampling variation across personas; they do not estimate generation-seed uncertainty. The separate multi-seed experiment is required for that reviewer concern.
