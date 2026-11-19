# Baseline comparison report

상태: **DATA_READY / MANUSCRIPT_EDIT_ONLY**. 아래 결과는 완료된 `20260913` run을 재사용했다. 모든 contrast는 `Dialogue-only Adaptive − comparator`, `N=304` pairs per target다.

## 공통 protocol

- 동일 304 frozen held-out personas
- 동일 target checkpoints와 Qwen3-14B interviewer/final predictor
- 동일 최초 question/response 문자열
- 5-turn fixed maximum; 이 run의 모든 baseline과 Adaptive가 실제 5 turns 사용
- 동일 graph extractor, final predictor, scoring, majority normalization
- 질문정책만 변경
- Main raw: `results/access_revision/main/raw/*/*.jsonl`
- Main aggregate: `results/access_revision/main/aggregate/`

## Baseline 정의

| Method | Protocol | External official reproduction? |
|---|---|---|
| `random_candidate` | Adaptive가 생성한 세 candidate 중 score를 보지 않고 deterministic pseudorandom index로 선택 | 해당 없음; local controlled ablation/baseline |
| `round_robin` | 질문 2–5를 social role → personality → background → interests 순으로 고정 | 해당 없음; local controlled baseline |
| `dialogue_followup` | 가장 최근 응답에 구체적 follow-up을 생성; ambiguity, coverage, candidates, target dimension 없음 | 해당 없음; local controlled baseline |
| `controller_matched_generic` | 3-candidate JSON controller와 token shape를 맞추되 specificity/repetition만 판단 | 해당 없음; local controlled baseline |
| `uncertainty_sampling` | 매 turn K=5 stochastic closed-set prediction의 normalized entropy가 가장 큰 dimension을 질문 | **Protocol adaptation**; Active-Prompt/GSM official implementation의 direct reproduction 아님 |

외부 active baseline의 direct compatible official implementation 결과: **`[MISSING]`**. 현재 결과는 `active-prompt-adapted-entropy-v1`이며 이 경계를 원고와 response에 그대로 밝혀야 한다.

## Active uncertainty protocol

- 매 turn 1–4 이후 Qwen3-14B가 dialogue-only closed-set prediction 5개 생성
- temperature 0.8, top-p 0.8, deterministic persona/turn/sample seed
- `U_d = H(p_hat_d)/log(|L_d|+1)`; `+1`은 invalid outcome
- 최대 entropy, least-asked dimension, fixed dimension order 순 tie-break
- graph와 hidden persona는 uncertainty predictor에 제공하지 않음
- 항상 5 questions, adaptive stopping 없음
- 상세: `docs/access_active_information_gain_baseline.md`

## Macro Average Gain 결과

CI는 10,000회 paired percentile bootstrap, p-value는 paired Wilcoxon이다. Main four-baseline macro family는 16 tests(4 targets × 4 baselines), active-primary macro family는 4 tests다. `effect`는 rank-biserial effect다.

| Target | Comparator | Δ | 95% CI | Raw p | BH p | Effect |
|---|---|---:|---:|---:|---:|---:|
| Qwen3-1.7B | random candidate | −0.0064 | [−0.0364, +0.0253] | 0.6225 | 0.7487 | −0.053 |
| Qwen3-1.7B | round robin | +0.0332 | [−0.0020, +0.0686] | 0.07242 | 0.1448 | +0.172 |
| Qwen3-1.7B | dialogue follow-up | +0.0232 | [−0.0088, +0.0566] | 0.1138 | 0.2023 | +0.172 |
| Qwen3-1.7B | controller-matched generic | +0.0110 | [−0.0266, +0.0477] | 0.6551 | 0.7487 | +0.045 |
| Qwen3-4B | random candidate | +0.0161 | [−0.0160, +0.0492] | 0.7662 | 0.8173 | +0.032 |
| Qwen3-4B | round robin | +0.0656 | [+0.0304, +0.1001] | 0.000376 | 0.001504 | +0.341 |
| Qwen3-4B | dialogue follow-up | +0.0629 | [+0.0267, +0.0986] | 0.001965 | 0.006289 | +0.296 |
| Qwen3-4B | controller-matched generic | +0.0470 | [+0.0153, +0.0791] | 0.007717 | 0.02058 | +0.277 |
| Llama-3.2-3B | random candidate | +0.0016 | [−0.0341, +0.0366] | 0.9946 | 0.9946 | +0.001 |
| Llama-3.2-3B | round robin | +0.0690 | [+0.0314, +0.1067] | 0.000310 | 0.001504 | +0.323 |
| Llama-3.2-3B | dialogue follow-up | +0.0755 | [+0.0350, +0.1153] | 0.000197 | 0.001504 | +0.341 |
| Llama-3.2-3B | controller-matched generic | +0.0832 | [+0.0470, +0.1194] | 0.000014 | 0.000231 | +0.393 |
| Gemma-3-4B | random candidate | −0.0235 | [−0.0591, +0.0122] | 0.1811 | 0.2898 | −0.132 |
| Gemma-3-4B | round robin | −0.0202 | [−0.0585, +0.0177] | 0.5668 | 0.7487 | −0.054 |
| Gemma-3-4B | dialogue follow-up | +0.0163 | [−0.0232, +0.0554] | 0.4768 | 0.6936 | +0.067 |
| Gemma-3-4B | controller-matched generic | +0.0243 | [−0.0125, +0.0621] | 0.06103 | 0.1395 | +0.183 |
| Qwen3-1.7B | active uncertainty | +0.0072 | [−0.0261, +0.0409] | 0.7088 | 0.7206 | +0.037 |
| Qwen3-4B | active uncertainty | −0.0022 | [−0.0366, +0.0309] | 0.7206 | 0.7206 | −0.035 |
| Llama-3.2-3B | active uncertainty | −0.0264 | [−0.0654, +0.0118] | 0.2947 | 0.5894 | −0.091 |
| Gemma-3-4B | active uncertainty | −0.0394 | [−0.0756, −0.0036] | 0.06943 | 0.2777 | −0.173 |

Full-precision dimension/McNemar 결과와 method means:

- `results/access_revision/main/aggregate/paired_tests.csv`
- `results/access_revision/main/aggregate/method_metrics.csv`
- `results/access_revision/active_information_gain/main/aggregate/paired_tests.csv`
- `results/access_revision/active_information_gain/main/aggregate/method_metrics.csv`

## 해석

- Adaptive는 Qwen3-4B와 Llama에서 round-robin, dialogue follow-up, controller-matched generic보다 높았다.
- Random candidate 대비 네 target 모두 BH 보정 후 유의하지 않았다. 따라서 candidate ranking 자체의 독립 우월성은 확인되지 않았다.
- Active uncertainty 대비 네 target 모두 BH 보정 후 유의하지 않았다. Gemma의 mean CI는 Adaptive에 불리한 방향으로 zero를 제외했지만 signed-rank raw/BH p-value는 유의하지 않았다. 두 요약의 불일치를 숨기지 않아야 한다.
- Qwen3-1.7B와 Gemma에서는 simple-baseline 대비 일관된 이득이 확인되지 않았다.

원고용 문장:

> Adaptive questioning outperformed several fixed or generic baselines for Qwen3-4B and Llama-3.2-3B, but it did not significantly outperform random candidate selection for any target. It also did not differ significantly from the adapted uncertainty-sampling baseline after correction. These results do not isolate a consistent benefit of the proposed candidate-ranking mechanism.

