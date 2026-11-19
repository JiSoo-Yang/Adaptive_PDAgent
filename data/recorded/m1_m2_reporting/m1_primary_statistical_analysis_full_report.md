# M1 primary statistical analysis full report

## 분석 대상과 contrast

- Target models: Qwen3-1.7B, Qwen3-4B, Llama-3.2-3B-Instruct, Gemma-3-4B-IT
- 각 target의 held-out persona: 304명
- 비교: Adaptive PD-Agent (`dialogue_only`) minus Original PD-Agent (`original`)
- 전체 paired 관측값: 4 × 304 = 1,216개
- 원자료 run seed: `20260831`
- held-out cohort seed: `20260802`
- persona별 Original Average Gain, Adaptive Average Gain, 차이값은 `m1_persona_level.csv`에 수록했다.

## 표에 바로 사용할 최종 요약

`N`은 전체 paired persona 수이고, `N_eff`는 `zero_method='wilcox'`가 zero difference를 제거한 뒤 signed-rank 계산에 사용한 nonzero pair 수다. `W`는 SciPy가 two-sided 검정에서 반환한 두 signed-rank 합 중 작은 값이다.

| Target | N | N_eff | Original Average Gain | Adaptive Average Gain | Δ Adaptive−Original | Paired-bootstrap 95% CI | W | Raw p | BH p | + / − / tie |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-1.7B | 304 | 117 | 0.2528 | 0.2718 | +0.0190 | [−0.0139, +0.0519] | 2994.0 | 0.211209 | 0.211209 | 63 / 54 / 187 |
| Qwen3-4B | 304 | 133 | 0.3179 | 0.3575 | +0.0397 | [+0.0046, +0.0753] | 3442.0 | 0.022351 | 0.030072 | 80 / 53 / 171 |
| Llama-3.2-3B-Instruct | 304 | 161 | 0.3364 | 0.3899 | +0.0536 | [+0.0181, +0.0901] | 4603.5 | 0.001188 | 0.004750 | 98 / 63 / 143 |
| Gemma-3-4B-IT | 304 | 153 | 0.3731 | 0.4013 | +0.0281 | [−0.0088, +0.0656] | 4641.5 | 0.022554 | 0.030072 | 81 / 72 / 151 |

기계 판독 가능한 full-precision 값은 `m1_primary_summary.csv`, LaTeX 행은 `m1_primary_summary_table.tex`에 있다.

## Wilcoxon 설정

- 입력 관측값: 각 target의 persona별 `Adaptive Average Gain − Original Average Gain`, 총 304개
- 구현 호출: `scipy.stats.wilcoxon(differences)`
- SciPy version: `1.17.1`
- `zero_method='wilcox'`: zero difference를 rank 계산에서 제거
- `alternative='two-sided'`
- `correction=False`
- 요청 method: `auto`
- 실제 method: 입력 길이 304가 SciPy 1.17.1의 50개 기준을 넘으므로 asymptotic
- raw p-value: 위 호출이 반환한 two-sided asymptotic p-value

전체 pair 수는 네 target 모두 304지만 zero difference가 많으므로 Wilcoxon의 effective nonzero sample은 각각 117, 133, 161, 153이다. 논문에는 두 수를 함께 제시하는 편이 정확하다.

## Paired bootstrap 설정

- 반복 횟수: 10,000
- CI: ordinary percentile 95% CI
- 각 반복에서 같은 target의 304개 persona index를 replacement로 304번 추출하고, 선택된 persona별 paired difference의 산술평균을 계산
- 하한/상한: 10,000개 평균의 2.5th/97.5th percentile
- BCa, studentization, finite-sample correction은 사용하지 않음

| Target | Bootstrap seed | Mean Δ | 95% CI |
|---|---:|---:|---:|
| Qwen3-1.7B | 20260917 | +0.018964 | [−0.013870, +0.051857] |
| Qwen3-4B | 20260927 | +0.039692 | [+0.004635, +0.075315] |
| Llama-3.2-3B-Instruct | 20260937 | +0.053559 | [+0.018113, +0.090120] |
| Gemma-3-4B-IT | 20260947 | +0.028137 | [−0.008839, +0.065591] |

## BH correction

- Family: `adaptive_vs_original_macro_gain_across_4_targets`
- Family size: 4
- 포함 검정: 네 target의 Adaptive-vs-Original Average Gain Wilcoxon 검정만 포함
- Dimension-level 16개 McNemar 검정은 별도의 family로 보정했으며 여기에 섞지 않음

| Target | Raw p | BH adjusted p |
|---|---:|---:|
| Qwen3-1.7B | 0.2112087764 | 0.2112087764 |
| Qwen3-4B | 0.0223512200 | 0.0300718477 |
| Llama-3.2-3B-Instruct | 0.0011875914 | 0.0047503654 |
| Gemma-3-4B-IT | 0.0225538858 | 0.0300718477 |

## 결과 해석

원고에 사용할 수 있는 보수적 해석은 다음과 같다.

> Adaptive PD-Agent had a positive mean persona-level Average Gain difference for all four target models. The paired-bootstrap 95% confidence interval excluded zero for Qwen3-4B and Llama-3.2-3B-Instruct. After Benjamini–Hochberg correction across the four target-level Wilcoxon tests, the signed-rank result was significant for Qwen3-4B, Llama-3.2-3B-Instruct, and Gemma-3-4B-IT, but not for Qwen3-1.7B.

## 과장 방지를 위한 limitation

- 결과는 target에 따라 다르다. Qwen3-1.7B는 mean difference가 양수지만 bootstrap CI가 zero를 포함하고 BH-adjusted Wilcoxon도 유의하지 않다.
- Gemma의 Wilcoxon BH p-value는 0.05보다 작지만 mean-difference bootstrap CI는 zero를 포함한다. Wilcoxon은 nonzero paired difference의 signed ranks를, bootstrap CI는 304개 차이의 평균을 요약하므로 두 결과가 반드시 같을 필요는 없다. Gemma에 대해 “평균 개선이 일관되게 확립됐다”고 단정하면 안 된다.
- Wilcoxon의 tie 수가 143–187로 많아 effective sample size는 전체 304보다 작다.
- 이 분석은 네 target을 각각 검정했으며 target을 하나의 모집단으로 합친 pooled effect나 model-level random-effects 분석은 수행하지 않았다.
- Average Gain은 held-out cohort에서 산출한 majority baseline에 의존하는 상대 지표다. 다른 persona 분포에서는 baseline과 gain 크기가 달라질 수 있다.
- 이 결과만으로 모든 persona dimension이 개선됐다고 해석할 수 없다. Dimension-level family에서 BH 보정 후 지지된 양의 차이는 Llama와 Gemma의 background뿐이다.
- 유의성 판정 기준 `α=0.05`가 기존 원고나 사전 protocol에 명시되어 있었는지는 `[MISSING]`다. 위 문장의 “significant”는 통상적인 0.05 기준을 적용한 서술이다.

