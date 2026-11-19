# Adapted uncertainty-sampling active baseline

This is a protocol adaptation, not a direct reproduction of an external codebase.
The exact first question and response are reused from each paired dialogue_only row.
After each of turns 1–4, the common Qwen3-14B predictor produces five
dialogue-only closed-set predictions at temperature 0.8. The policy selects
the dimension with maximum normalized empirical entropy; ties go to the
least-asked dimension and then fixed schema order. Interaction remains five turns.

Methodological sources:
- Active-Prompt: https://github.com/shizhediao/active-prompt
- Active Feature Acquisition with Generative Surrogate Models: 
  https://proceedings.mlr.press/v139/li21p.html

## Dialogue-only Adaptive versus uncertainty sampling

| Target | Δ Average Gain | 95% CI | raw p | BH p | + / − / tie |
|---|---:|---:|---:|---:|---:|
| Qwen/Qwen3-1.7B | +0.0072 | [-0.0261, +0.0409] | 0.7088 | 0.7206 | 69 / 62 / 173 |
| Qwen/Qwen3-4B | -0.0022 | [-0.0366, +0.0309] | 0.7206 | 0.7206 | 70 / 67 / 167 |
| meta-llama/Llama-3.2-3B-Instruct | -0.0264 | [-0.0654, +0.0118] | 0.2947 | 0.5894 | 85 / 89 / 130 |
| google/gemma-3-4b-it | -0.0394 | [-0.0756, -0.0036] | 0.06943 | 0.2777 | 63 / 82 / 159 |

## Method means and cost

| Target | Method | Macro gain | Input tokens | Output tokens | Calls |
|---|---|---:|---:|---:|---:|
| Qwen/Qwen3-1.7B | original | 0.2187 | 6008 | 2006 | 16 |
| Qwen/Qwen3-1.7B | dialogue_only | 0.2499 | 6089 | 2574 | 16 |
| Qwen/Qwen3-1.7B | random_candidate | 0.2563 | 6098 | 2556 | 16 |
| Qwen/Qwen3-1.7B | round_robin | 0.2167 | 6069 | 2010 | 16 |
| Qwen/Qwen3-1.7B | uncertainty_sampling | 0.2427 | 15127 | 3293 | 36 |
| Qwen/Qwen3-4B | original | 0.3077 | 5980 | 2076 | 16 |
| Qwen/Qwen3-4B | dialogue_only | 0.3871 | 6177 | 2662 | 16 |
| Qwen/Qwen3-4B | random_candidate | 0.3709 | 6160 | 2660 | 16 |
| Qwen/Qwen3-4B | round_robin | 0.3215 | 6091 | 2102 | 16 |
| Qwen/Qwen3-4B | uncertainty_sampling | 0.3893 | 15161 | 3444 | 36 |
| meta-llama/Llama-3.2-3B-Instruct | original | 0.3240 | 7372 | 2527 | 16 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only | 0.4105 | 7430 | 3119 | 16 |
| meta-llama/Llama-3.2-3B-Instruct | random_candidate | 0.4090 | 7429 | 3114 | 16 |
| meta-llama/Llama-3.2-3B-Instruct | round_robin | 0.3416 | 7377 | 2515 | 16 |
| meta-llama/Llama-3.2-3B-Instruct | uncertainty_sampling | 0.4370 | 17683 | 3835 | 36 |
| google/gemma-3-4b-it | original | 0.3521 | 7179 | 2447 | 16 |
| google/gemma-3-4b-it | dialogue_only | 0.3805 | 7378 | 3090 | 16 |
| google/gemma-3-4b-it | random_candidate | 0.4041 | 7302 | 3048 | 16 |
| google/gemma-3-4b-it | round_robin | 0.4007 | 7418 | 2501 | 16 |
| google/gemma-3-4b-it | uncertainty_sampling | 0.4199 | 17585 | 3768 | 36 |

## Uncertainty target distribution

| Target | Dimension | Selected | Rate | Mean normalized entropy |
|---|---|---:|---:|---:|
| Qwen/Qwen3-1.7B | social_role | 335/1216 | 0.275 | 0.022 |
| Qwen/Qwen3-1.7B | personality | 290/1216 | 0.238 | 0.014 |
| Qwen/Qwen3-1.7B | background | 347/1216 | 0.285 | 0.052 |
| Qwen/Qwen3-1.7B | interests | 244/1216 | 0.201 | 0.022 |
| Qwen/Qwen3-4B | social_role | 320/1216 | 0.263 | 0.011 |
| Qwen/Qwen3-4B | personality | 290/1216 | 0.238 | 0.010 |
| Qwen/Qwen3-4B | background | 363/1216 | 0.299 | 0.050 |
| Qwen/Qwen3-4B | interests | 243/1216 | 0.200 | 0.020 |
| meta-llama/Llama-3.2-3B-Instruct | social_role | 312/1216 | 0.257 | 0.009 |
| meta-llama/Llama-3.2-3B-Instruct | personality | 295/1216 | 0.243 | 0.013 |
| meta-llama/Llama-3.2-3B-Instruct | background | 363/1216 | 0.299 | 0.048 |
| meta-llama/Llama-3.2-3B-Instruct | interests | 246/1216 | 0.202 | 0.019 |
| google/gemma-3-4b-it | social_role | 314/1216 | 0.258 | 0.013 |
| google/gemma-3-4b-it | personality | 290/1216 | 0.238 | 0.009 |
| google/gemma-3-4b-it | background | 378/1216 | 0.311 | 0.053 |
| google/gemma-3-4b-it | interests | 234/1216 | 0.192 | 0.015 |
