# Dimension-level statistical test report

## Paired binary outcome와 검정 정의

각 target, persona, dimension에 대해 Original correctness `O_i ∈ {0,1}`와 Adaptive correctness `A_i ∈ {0,1}`를 만든다.

- `both correct`: `(O_i, A_i) = (1,1)`
- `b`: Original correct, Adaptive incorrect `(1,0)` — Adaptive loss
- `c`: Original incorrect, Adaptive correct `(0,1)` — Adaptive gain
- `both incorrect`: `(0,0)`

McNemar 검정은 discordant pair `b+c`만 사용한다. 완료된 분석은 `c ~ Binomial(b+c, 0.5)`의 **exact two-sided binomial test**이며 continuity correction이나 asymptotic chi-square approximation을 쓰지 않았다. Accuracy difference는 `(c−b)/304`다.

## 전체 결과

`BC`는 both correct, `BI`는 both incorrect다. 모든 행의 `N=304`다.

| Target | Dimension | BC | b | c | BI | Adaptive−Original accuracy | Raw p | BH p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-1.7B | Social role | 213 | 10 | 16 | 65 | +0.0197 | 0.326940 | 0.569496 |
| Qwen3-1.7B | Personality | 155 | 14 | 20 | 115 | +0.0197 | 0.391528 | 0.569496 |
| Qwen3-1.7B | Background | 72 | 14 | 15 | 203 | +0.0033 | 1.000000 | 1.000000 |
| Qwen3-1.7B | Interests | 146 | 26 | 25 | 107 | −0.0033 | 1.000000 | 1.000000 |
| Qwen3-4B | Social role | 262 | 7 | 15 | 20 | +0.0263 | 0.133801 | 0.356801 |
| Qwen3-4B | Personality | 157 | 21 | 19 | 107 | −0.0066 | 0.874629 | 1.000000 |
| Qwen3-4B | Background | 75 | 17 | 33 | 179 | +0.0526 | 0.032839 | 0.131357 |
| Qwen3-4B | Interests | 135 | 19 | 32 | 118 | +0.0428 | 0.091915 | 0.294127 |
| Llama-3.2-3B-Instruct | Social role | 245 | 13 | 17 | 29 | +0.0132 | 0.584665 | 0.779553 |
| Llama-3.2-3B-Instruct | Personality | 171 | 21 | 30 | 82 | +0.0296 | 0.262438 | 0.569496 |
| Llama-3.2-3B-Instruct | Background | 80 | 18 | 48 | 158 | +0.0987 | 0.000287 | 0.004594 |
| Llama-3.2-3B-Instruct | Interests | 119 | 36 | 34 | 115 | −0.0066 | 0.904975 | 1.000000 |
| Gemma-3-4B-IT | Social role | 236 | 13 | 19 | 36 | +0.0197 | 0.377086 | 0.569496 |
| Gemma-3-4B-IT | Personality | 181 | 19 | 26 | 78 | +0.0230 | 0.371298 | 0.569496 |
| Gemma-3-4B-IT | Background | 85 | 16 | 41 | 162 | +0.0822 | 0.001264 | 0.010108 |
| Gemma-3-4B-IT | Interests | 142 | 41 | 22 | 99 | −0.0625 | 0.022575 | 0.120400 |

Original/Adaptive accuracy, paired-bootstrap CI, bootstrap seed와 full-precision p-value는 `dimension_level_tests.csv`에 있다.

## Multiple-comparison correction

- Correction: Benjamini–Hochberg
- Family: `adaptive_vs_original_4_dimensions_across_4_targets`
- Family size: 16, 즉 4 targets × 4 dimensions
- M1 Average Gain의 네 Wilcoxon 검정은 별도 4-test family이므로 이 16개와 섞지 않았다.

통상적인 `α=0.05` 기준에서 BH 보정 후 지지되는 결과는 두 개다.

- Llama background: `b=18`, `c=48`, Δ accuracy `+0.0987`, raw `p=0.000287`, BH `p=0.004594`
- Gemma background: `b=16`, `c=41`, Δ accuracy `+0.0822`, raw `p=0.001264`, BH `p=0.010108`

Qwen3-4B background의 raw p-value는 0.0328이지만 16-test BH 보정 후 0.1314다. Gemma interests는 음의 difference와 raw p-value 0.0226을 보였지만 BH p-value는 0.1204다.

## Dimension-level paired Wilcoxon

완료된 M1 분석에는 dimension별 Wilcoxon 결과가 없다. 네 dimension의 persona score가 이 자료에서 binary이므로 prespecified dimension-level 분석은 exact McNemar였다. 사용자가 요청한 “있다면 제시” 조건에 따라, 새로운 검정을 임의로 추가하지 않았다.

## 해석 지침

- Background에서의 개선이 가장 분명하다. 다만 4개 target 중 Llama와 Gemma에서만 family-wise BH 결과가 0.05보다 작다.
- Social role과 personality는 일부 target에서 양의 point estimate가 있지만 16-test family에서 통계적 근거가 확인되지 않았다.
- Interests는 target별 방향이 다르다. Qwen3-4B는 양의 point estimate, Llama와 Qwen3-1.7B는 거의 zero, Gemma는 음의 point estimate다.
- 따라서 “Adaptive improves all four dimensions” 또는 “the improvement is uniform across models”이라고 쓰면 안 된다.
- BH p-value가 0.05 이상인 결과를 “차이가 없다”고 단정하면 안 된다. 이 분석이 해당 차이를 검출할 충분한 근거를 제공하지 못했다고 기술해야 한다.
- `α=0.05`가 기존 원고나 사전 protocol에 명시돼 있었는지는 `[MISSING]`다.

