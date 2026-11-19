# IEEE Access additional-baseline experiment

Each cell contains 304 paired held-out personas at a five-turn maximum.
The initial question and response use the same realization within each paired set,
and all methods use the same graph extractor and final predictor.

## Macro-gain comparisons

| Target | Contrast | Δ | 95% CI | BH p | + / − / tie |
|---|---|---:|---:|---:|---:|
| Qwen/Qwen3-1.7B | dialogue_only - random_candidate | -0.0064 | [-0.0364, +0.0253] | 0.7487 | 51 / 61 / 192 |
| Qwen/Qwen3-1.7B | dialogue_only - round_robin | +0.0332 | [-0.0020, +0.0686] | 0.1448 | 80 / 64 / 160 |
| Qwen/Qwen3-1.7B | dialogue_only - dialogue_followup | +0.0232 | [-0.0088, +0.0566] | 0.2023 | 58 / 53 / 193 |
| Qwen/Qwen3-1.7B | dialogue_only - controller_matched_generic | +0.0110 | [-0.0266, +0.0477] | 0.7487 | 66 / 66 / 172 |
| Qwen/Qwen3-1.7B | dialogue_only - adaptive_direct | +0.0059 | [-0.0258, +0.0384] | 0.9848 | 61 / 60 / 183 |
| Qwen/Qwen3-1.7B | dialogue_only - adaptive_no_coverage | +0.0017 | [-0.0295, +0.0325] | 0.9974 | 50 / 55 / 199 |
| Qwen/Qwen3-1.7B | dialogue_only - adaptive_no_redundancy | +0.0276 | [-0.0031, +0.0575] | 0.3331 | 66 / 42 / 196 |
| Qwen/Qwen3-1.7B | dialogue_only - original | +0.0311 | [-0.0037, +0.0654] | 0.1087 | 73 / 60 / 171 |
| Qwen/Qwen3-4B | dialogue_only - random_candidate | +0.0161 | [-0.0160, +0.0492] | 0.8173 | 63 / 53 / 188 |
| Qwen/Qwen3-4B | dialogue_only - round_robin | +0.0656 | [+0.0304, +0.1001] | 0.001504 | 92 / 51 / 161 |
| Qwen/Qwen3-4B | dialogue_only - dialogue_followup | +0.0629 | [+0.0267, +0.0986] | 0.006289 | 91 / 53 / 160 |
| Qwen/Qwen3-4B | dialogue_only - controller_matched_generic | +0.0470 | [+0.0153, +0.0791] | 0.02058 | 79 / 43 / 182 |
| Qwen/Qwen3-4B | dialogue_only - adaptive_direct | +0.0309 | [-0.0016, +0.0639] | 0.3331 | 70 / 55 / 179 |
| Qwen/Qwen3-4B | dialogue_only - adaptive_no_coverage | +0.0044 | [-0.0263, +0.0365] | 0.9848 | 59 / 61 / 184 |
| Qwen/Qwen3-4B | dialogue_only - adaptive_no_redundancy | +0.0131 | [-0.0182, +0.0443] | 0.9848 | 59 / 60 / 185 |
| Qwen/Qwen3-4B | dialogue_only - original | +0.0793 | [+0.0450, +0.1138] | 2.779e-05 | 97 / 47 / 160 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - random_candidate | +0.0016 | [-0.0341, +0.0366] | 0.9946 | 63 / 70 / 171 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - round_robin | +0.0690 | [+0.0314, +0.1067] | 0.001504 | 102 / 63 / 139 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - dialogue_followup | +0.0755 | [+0.0350, +0.1153] | 0.001504 | 97 / 61 / 146 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - controller_matched_generic | +0.0832 | [+0.0470, +0.1194] | 0.0002314 | 105 / 56 / 143 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - adaptive_direct | +0.0129 | [-0.0236, +0.0499] | 0.9848 | 77 / 74 / 153 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - adaptive_no_coverage | -0.0024 | [-0.0369, +0.0324] | 0.9848 | 64 / 69 / 171 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - adaptive_no_redundancy | +0.0143 | [-0.0203, +0.0486] | 0.9022 | 77 / 59 / 168 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only - original | +0.0865 | [+0.0486, +0.1246] | 2.133e-05 | 104 / 60 / 140 |
| google/gemma-3-4b-it | dialogue_only - random_candidate | -0.0235 | [-0.0591, +0.0122] | 0.2898 | 64 / 72 / 168 |
| google/gemma-3-4b-it | dialogue_only - round_robin | -0.0202 | [-0.0585, +0.0177] | 0.7487 | 70 / 77 / 157 |
| google/gemma-3-4b-it | dialogue_only - dialogue_followup | +0.0163 | [-0.0232, +0.0554] | 0.6936 | 81 / 70 / 153 |
| google/gemma-3-4b-it | dialogue_only - controller_matched_generic | +0.0243 | [-0.0125, +0.0621] | 0.1395 | 71 / 68 / 165 |
| google/gemma-3-4b-it | dialogue_only - adaptive_direct | +0.0113 | [-0.0246, +0.0490] | 0.9848 | 79 / 68 / 157 |
| google/gemma-3-4b-it | dialogue_only - adaptive_no_coverage | +0.0203 | [-0.0134, +0.0544] | 0.9022 | 67 / 61 / 176 |
| google/gemma-3-4b-it | dialogue_only - adaptive_no_redundancy | +0.0237 | [-0.0113, +0.0590] | 0.9022 | 77 / 64 / 163 |
| google/gemma-3-4b-it | dialogue_only - original | +0.0285 | [-0.0087, +0.0654] | 0.1347 | 81 / 61 / 162 |

## Method means

| Target | Method | Macro gain | Turns | Input tokens | Output tokens |
|---|---|---:|---:|---:|---:|
| Qwen/Qwen3-1.7B | original | 0.2187 | 5.00 | 6008 | 2006 |
| Qwen/Qwen3-1.7B | dialogue_only | 0.2499 | 5.00 | 6089 | 2574 |
| Qwen/Qwen3-1.7B | random_candidate | 0.2563 | 5.00 | 6098 | 2556 |
| Qwen/Qwen3-1.7B | round_robin | 0.2167 | 5.00 | 6069 | 2010 |
| Qwen/Qwen3-1.7B | dialogue_followup | 0.2267 | 5.00 | 5909 | 1968 |
| Qwen/Qwen3-1.7B | controller_matched_generic | 0.2389 | 5.00 | 6206 | 2661 |
| Qwen/Qwen3-1.7B | adaptive_direct | 0.2440 | 5.00 | 5955 | 2064 |
| Qwen/Qwen3-1.7B | adaptive_no_coverage | 0.2482 | 5.00 | 5987 | 2428 |
| Qwen/Qwen3-1.7B | adaptive_no_redundancy | 0.2223 | 5.00 | 5976 | 2391 |
| Qwen/Qwen3-4B | original | 0.3077 | 5.00 | 5980 | 2076 |
| Qwen/Qwen3-4B | dialogue_only | 0.3871 | 5.00 | 6177 | 2662 |
| Qwen/Qwen3-4B | random_candidate | 0.3709 | 5.00 | 6160 | 2660 |
| Qwen/Qwen3-4B | round_robin | 0.3215 | 5.00 | 6091 | 2102 |
| Qwen/Qwen3-4B | dialogue_followup | 0.3241 | 5.00 | 5962 | 2073 |
| Qwen/Qwen3-4B | controller_matched_generic | 0.3401 | 5.00 | 6260 | 2774 |
| Qwen/Qwen3-4B | adaptive_direct | 0.3562 | 5.00 | 6079 | 2191 |
| Qwen/Qwen3-4B | adaptive_no_coverage | 0.3827 | 5.00 | 6074 | 2533 |
| Qwen/Qwen3-4B | adaptive_no_redundancy | 0.3740 | 5.00 | 6077 | 2506 |
| meta-llama/Llama-3.2-3B-Instruct | original | 0.3240 | 5.00 | 7372 | 2527 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_only | 0.4105 | 5.00 | 7430 | 3119 |
| meta-llama/Llama-3.2-3B-Instruct | random_candidate | 0.4090 | 5.00 | 7429 | 3114 |
| meta-llama/Llama-3.2-3B-Instruct | round_robin | 0.3416 | 5.00 | 7377 | 2515 |
| meta-llama/Llama-3.2-3B-Instruct | dialogue_followup | 0.3350 | 5.00 | 7277 | 2500 |
| meta-llama/Llama-3.2-3B-Instruct | controller_matched_generic | 0.3273 | 5.00 | 7584 | 3224 |
| meta-llama/Llama-3.2-3B-Instruct | adaptive_direct | 0.3976 | 5.00 | 7330 | 2626 |
| meta-llama/Llama-3.2-3B-Instruct | adaptive_no_coverage | 0.4129 | 5.00 | 7313 | 2989 |
| meta-llama/Llama-3.2-3B-Instruct | adaptive_no_redundancy | 0.3962 | 5.00 | 7299 | 2948 |
| google/gemma-3-4b-it | original | 0.3521 | 5.00 | 7179 | 2447 |
| google/gemma-3-4b-it | dialogue_only | 0.3805 | 5.00 | 7378 | 3090 |
| google/gemma-3-4b-it | random_candidate | 0.4041 | 5.00 | 7302 | 3048 |
| google/gemma-3-4b-it | round_robin | 0.4007 | 5.00 | 7418 | 2501 |
| google/gemma-3-4b-it | dialogue_followup | 0.3642 | 5.00 | 7248 | 2478 |
| google/gemma-3-4b-it | controller_matched_generic | 0.3562 | 5.00 | 8006 | 3355 |
| google/gemma-3-4b-it | adaptive_direct | 0.3692 | 5.00 | 7239 | 2584 |
| google/gemma-3-4b-it | adaptive_no_coverage | 0.3603 | 5.00 | 7274 | 2963 |
| google/gemma-3-4b-it | adaptive_no_redundancy | 0.3568 | 5.00 | 7217 | 2905 |
