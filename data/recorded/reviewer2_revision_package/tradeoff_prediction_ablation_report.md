# Trade-off, prediction-validity, budget, and ablation report

상태: **DATA_READY / MANUSCRIPT_EDIT_ONLY**. Prediction-validity와 budget-allocation에는 완료된 inferential CI/test가 없으므로 해당 위치를 `[MISSING]`으로 표시한다.

## Raw dimension metric과 Average Gain

아래는 `20260913`, N=304/cell의 raw persona accuracy/F1 mean과 Average Gain이다. SR=coarse social-role accuracy, P=personality accuracy, B=background value accuracy, I=singleton-interest F1/accuracy다.

| Target | Method | SR | P | B | I | Average Gain |
|---|---|---:|---:|---:|---:|---:|
| Qwen3-1.7B | Adaptive | 0.6974 | 0.5526 | 0.3257 | 0.5625 | 0.2499 |
| Qwen3-1.7B | Random candidate | 0.7007 | 0.5559 | 0.3224 | 0.5757 | 0.2563 |
| Qwen3-1.7B | Direct generation | 0.6875 | 0.5559 | 0.2862 | 0.5921 | 0.2440 |
| Qwen3-1.7B | No coverage | 0.6941 | 0.5625 | 0.2993 | 0.5724 | 0.2482 |
| Qwen3-1.7B | No redundancy | 0.6908 | 0.5362 | 0.2895 | 0.5526 | 0.2223 |
| Qwen3-4B | Adaptive | 0.9145 | 0.6020 | 0.3553 | 0.5954 | 0.3871 |
| Qwen3-4B | Random candidate | 0.9178 | 0.6020 | 0.3816 | 0.5164 | 0.3709 |
| Qwen3-4B | Direct generation | 0.8980 | 0.5888 | 0.3191 | 0.5822 | 0.3562 |
| Qwen3-4B | No coverage | 0.9046 | 0.6151 | 0.3684 | 0.5592 | 0.3827 |
| Qwen3-4B | No redundancy | 0.9178 | 0.6020 | 0.3520 | 0.5559 | 0.3740 |
| Llama-3.2-3B | Adaptive | 0.8750 | 0.6447 | 0.4178 | 0.5789 | 0.4105 |
| Llama-3.2-3B | Random candidate | 0.8816 | 0.6513 | 0.4046 | 0.5691 | 0.4090 |
| Llama-3.2-3B | Direct generation | 0.8947 | 0.6579 | 0.3520 | 0.5625 | 0.3976 |
| Llama-3.2-3B | No coverage | 0.8980 | 0.6480 | 0.4178 | 0.5526 | 0.4129 |
| Llama-3.2-3B | No redundancy | 0.8684 | 0.6546 | 0.3684 | 0.5789 | 0.3962 |
| Gemma-3-4B | Adaptive | 0.8257 | 0.6513 | 0.3980 | 0.5592 | 0.3805 |
| Gemma-3-4B | Random candidate | 0.8191 | 0.6743 | 0.4276 | 0.5691 | 0.4041 |
| Gemma-3-4B | Direct generation | 0.8158 | 0.6809 | 0.3586 | 0.5296 | 0.3692 |
| Gemma-3-4B | No coverage | 0.8322 | 0.6579 | 0.3914 | 0.4868 | 0.3603 |
| Gemma-3-4B | No redundancy | 0.8257 | 0.6447 | 0.3750 | 0.5230 | 0.3568 |

모든 9개 method의 raw score, normalized gain, turns, tokens는 `results/access_revision/main/aggregate/method_metrics.csv`에 있다.

## Controller ablation paired results

모든 Δ는 `Adaptive − ablation`이다. CI는 10,000회 paired percentile bootstrap, raw p는 paired Wilcoxon, BH family는 12 macro tests(4 targets × 3 ablations)다.

| Target | Ablation | Δ | 95% CI | Raw p | BH p | Rank-biserial |
|---|---|---:|---:|---:|---:|---:|
| Qwen3-1.7B | Direct generation | +0.0059 | [−0.0258, +0.0384] | 0.5863 | 0.9848 | +0.057 |
| Qwen3-1.7B | No coverage | +0.0017 | [−0.0295, +0.0325] | 0.9974 | 0.9974 | +0.000 |
| Qwen3-1.7B | No redundancy | +0.0276 | [−0.0031, +0.0575] | 0.05552 | 0.3331 | +0.211 |
| Qwen3-4B | Direct generation | +0.0309 | [−0.0016, +0.0639] | 0.03895 | 0.3331 | +0.212 |
| Qwen3-4B | No coverage | +0.0044 | [−0.0263, +0.0365] | 0.9028 | 0.9848 | −0.013 |
| Qwen3-4B | No redundancy | +0.0131 | [−0.0182, +0.0443] | 0.5477 | 0.9848 | +0.063 |
| Llama-3.2-3B | Direct generation | +0.0129 | [−0.0236, +0.0499] | 0.7836 | 0.9848 | +0.026 |
| Llama-3.2-3B | No coverage | −0.0024 | [−0.0369, +0.0324] | 0.8624 | 0.9848 | −0.017 |
| Llama-3.2-3B | No redundancy | +0.0143 | [−0.0203, +0.0486] | 0.3759 | 0.9022 | +0.087 |
| Gemma-3-4B | Direct generation | +0.0113 | [−0.0246, +0.0490] | 0.6697 | 0.9848 | +0.040 |
| Gemma-3-4B | No coverage | +0.0203 | [−0.0134, +0.0544] | 0.3467 | 0.9022 | +0.096 |
| Gemma-3-4B | No redundancy | +0.0237 | [−0.0113, +0.0590] | 0.2498 | 0.9022 | +0.111 |

12개 중 BH 보정 후 유의한 결과가 없다. Coverage, redundancy, candidate generation/ranking 각각의 독립 기여가 확립됐다고 주장하면 안 된다.

Random candidate는 ranking ablation 역할도 한다. Adaptive−Random macro Δ는 Qwen3-1.7B −0.0064, Qwen3-4B +0.0161, Llama +0.0016, Gemma −0.0235이며 네 target 모두 BH p≥0.2898이다. 자세한 값은 `baseline_comparison_report.md`에 있다.

## Dimension-level trade-off

기존 primary seed의 exact McNemar 16-test family에서는 Llama background와 Gemma background만 BH 0.05 아래였다. Interests는 target별 방향이 일치하지 않았고 Gemma에서는 음의 point estimate였다. 상세 b/c count, raw/BH p와 CI는 다음에 있다.

- `results/access_revision/m1_m2_reporting/dimension_level_statistical_test_report.md`
- `results/access_revision/m1_m2_reporting/dimension_level_tests.csv`
- Revision baseline/ablation의 모든 dimension contrast: `results/access_revision/main/aggregate/paired_tests.csv`

## Budget allocation

아래 count는 question text를 사람이 분류한 것이 아니라 controller가 저장한 `target_dimension` 4,864 follow-up decisions의 선언값이다. Original, dialogue follow-up, controller-matched generic은 target dimension을 정의하지 않는다.

| Method | Social role | Personality | Background | Interests | Unlabeled |
|---|---:|---:|---:|---:|---:|
| Adaptive | 241 (5.0%) | 187 (3.8%) | 933 (19.2%) | 3,503 (72.0%) | 0 |
| Random candidate | 330 (6.8%) | 191 (3.9%) | 1,015 (20.9%) | 3,327 (68.4%) | 1 |
| Round robin | 1,216 (25.0%) | 1,216 (25.0%) | 1,216 (25.0%) | 1,216 (25.0%) | 0 |
| Direct generation | 373 (7.7%) | 138 (2.8%) | 332 (6.8%) | 4,021 (82.7%) | 0 |
| No coverage | 351 (7.2%) | 52 (1.1%) | 876 (18.0%) | 3,580 (73.6%) | 5 |
| No redundancy | 141 (2.9%) | 136 (2.8%) | 424 (8.7%) | 4,163 (85.6%) | 0 |
| Active uncertainty | 1,281 (26.3%) | 1,165 (24.0%) | 1,451 (29.8%) | 967 (19.9%) | 0 |

Adaptive가 social-role evidence에 budget을 몰았다는 가설은 controller label 기준으로 지지되지 않는다. Adaptive의 선언 target은 interests에 집중됐다. 다만 question content의 독립 human annotation은 없으므로 allocation label의 타당성 CI/test는 **`[MISSING]`**이다. Full data는 `budget_allocation.csv`에 있다.

## Prediction validity

Main 10,944 rows의 43,776 dimension predictions 중 invalid field는 1,310개, 즉 2.9925%다. Method별 invalid rate:

| Method | Invalid / fields | Rate |
|---|---:|---:|
| Original | 119 / 4,864 | 2.45% |
| Adaptive | 179 / 4,864 | 3.68% |
| Random candidate | 148 / 4,864 | 3.04% |
| Round robin | 118 / 4,864 | 2.43% |
| Dialogue follow-up | 101 / 4,864 | 2.08% |
| Controller-matched generic | 109 / 4,864 | 2.24% |
| Direct generation | 170 / 4,864 | 3.50% |
| No coverage | 171 / 4,864 | 3.52% |
| No redundancy | 195 / 4,864 | 4.01% |

Dimension별로는 social role 1.64%, personality 0%, background 1.16%, interests 9.17%다. Invalid prediction은 scoring에서 correct로 간주되지 않는다. Prediction-validity rate의 CI와 method 간 paired significance test는 완료 분석에 없어 **`[MISSING]`**이다. 이는 descriptive audit로 보고해야 한다.

근거: `results/access_revision/audit/prediction_validity.csv`, `results/access_revision/audit/resource_and_reproducibility.json`.

## 결론에 사용할 제한 문장

> The controller reallocated most declared follow-up targets toward interests rather than social role, but these target labels were generated by the controller and were not independently annotated. Component ablations did not isolate significant benefits of candidate generation, coverage scoring, redundancy scoring, or ranking after multiple-comparison correction. Invalid predictions were concentrated in the interests field, so practical interpretation should accompany normalized-gain results with raw metrics and validity rates.

