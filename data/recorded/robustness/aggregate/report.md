# Generation-seed and PD-Agent-backbone robustness

## Three-seed Adaptive minus Original effects (N=100 per seed)

| Target | Seed | Δ Average Gain | 95% CI |
|---|---:|---:|---:|
| Qwen/Qwen3-1.7B | 20260831 | +0.0134 | [-0.0450, +0.0727] |
| Qwen/Qwen3-4B | 20260831 | +0.0665 | [-0.0013, +0.1313] |
| meta-llama/Llama-3.2-3B-Instruct | 20260831 | +0.0578 | [-0.0047, +0.1155] |
| google/gemma-3-4b-it | 20260831 | +0.0295 | [-0.0360, +0.0957] |
| Qwen/Qwen3-1.7B | 20260913 | +0.0003 | [-0.0620, +0.0649] |
| Qwen/Qwen3-4B | 20260913 | +0.0702 | [+0.0097, +0.1310] |
| meta-llama/Llama-3.2-3B-Instruct | 20260913 | +0.0505 | [-0.0176, +0.1174] |
| google/gemma-3-4b-it | 20260913 | +0.0122 | [-0.0533, +0.0780] |
| Qwen/Qwen3-1.7B | 20260914 | +0.0458 | [-0.0127, +0.1049] |
| Qwen/Qwen3-4B | 20260914 | +0.0723 | [+0.0110, +0.1319] |
| meta-llama/Llama-3.2-3B-Instruct | 20260914 | +0.0941 | [+0.0276, +0.1617] |
| google/gemma-3-4b-it | 20260914 | +0.0312 | [-0.0478, +0.1093] |

## Alternative PD-Agent backbone

| PD-Agent | Δ Average Gain | 95% CI |
|---|---:|---:|
| Qwen/Qwen3-14B | +0.0003 | [-0.0620, +0.0649] |
| Qwen/Qwen3-8B | -0.0035 | [-0.0605, +0.0530] |

Difference in method effects (8B − 14B): -0.0038 [-0.0936, +0.0834], p=0.9147.
