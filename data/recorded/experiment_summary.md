# IEEE Access 재투고 보완 실험 최종 요약

대상: Manuscript ID `Access-2026-38546` 결정문. 자동화 가능한 보완 실험은 모두 완료했다. Bridging graph의 의미적 타당도와 annotator agreement는 두 사람의 독립 판정이 필요하므로 annotation pack까지만 준비했다.

## 완료 범위

| 항목 | 설계 | 상태 |
|---|---|---|
| Adaptive vs Original 주 비교 | 4 target × 304 held-out persona, paired bootstrap 10,000회, Wilcoxon, positive/negative/tie, 4-target BH family | 완료 |
| 이진 차원별 비교 | social role/personality/background/interests, exact McNemar, 16-test BH family | 완료 |
| Strong baselines | random candidate, round-robin, dialogue follow-up, controller-matched generic | 완료: 4 targets × 4 methods × 304 rows |
| 외부 active 정보획득 baseline | Active-Prompt식 K=5 반복 예측 엔트로피로 다음 persona 차원 선택, 고정 5턴 | 완료: 4 targets × 304 rows; protocol adaptation |
| Controller ablations | direct generation, no coverage, no redundancy; random candidate가 ranking ablation | 완료: 4 targets × 3 methods × 304 rows |
| Generation-seed robustness | seed 20260831/20260913/20260914, target별 동일 100 persona, Original/Adaptive | 완료: 2,400 rows |
| Alternative backbone | PD-Agent Qwen3-8B vs Qwen3-14B, Qwen3-1.7B target, 동일 100 persona | 완료: 신규 200 rows |
| Dimension trade-off/seed disagreement | 차원별 정확도·gain·prediction entropy·invalid rate | 완료 |
| 비용·재현성 | checkpoint revision, 실제 call 설정, token, model call, wall time, GPU-hour, software | 완료 |
| 정성 사례 | target별 최대 개선/악화 paired 사례와 질문·graph·예측 | 완료 |
| Graph semantic validity | relation type 7종 × 20 edge = 140 edge, 2인 독립 annotation 양식 | 사람 판정 대기 |

## Adaptive vs Original

### 기존 seed 20260831, N=304

| Target | Δ Average Gain | paired-bootstrap 95% CI | BH p | + / − / tie |
|---|---:|---:|---:|---:|
| Qwen3-1.7B | +0.0190 | [-0.0139, +0.0519] | 0.2112 | 63 / 54 / 187 |
| Qwen3-4B | +0.0397 | [+0.0046, +0.0753] | 0.0301 | 80 / 53 / 171 |
| Llama-3.2-3B | +0.0536 | [+0.0181, +0.0901] | 0.0048 | 98 / 63 / 143 |
| Gemma-3-4B | +0.0281 | [-0.0088, +0.0656] | 0.0301 | 81 / 72 / 151 |

Gemma는 Wilcoxon BH p가 0.05 미만이지만 mean-difference bootstrap CI가 0을 포함한다. 일관된 유의 개선으로 표현하면 안 된다.

### 신규 seed 20260913, N=304

| Target | Δ Average Gain | paired-bootstrap 95% CI | BH p | + / − / tie |
|---|---:|---:|---:|---:|
| Qwen3-1.7B | +0.0311 | [-0.0037, +0.0654] | 0.1087 | 73 / 60 / 171 |
| Qwen3-4B | +0.0793 | [+0.0450, +0.1138] | 2.78e-5 | 97 / 47 / 160 |
| Llama-3.2-3B | +0.0865 | [+0.0486, +0.1246] | 2.13e-5 | 104 / 60 / 140 |
| Gemma-3-4B | +0.0285 | [-0.0087, +0.0654] | 0.1347 | 81 / 61 / 162 |

두 N=304 seed에서 Qwen3-4B와 Llama만 bootstrap CI가 모두 0보다 높다. Qwen3-1.7B와 Gemma의 평균 효과는 양수지만 불확실하다.

## Strong baseline 결과

아래 값은 신규 seed에서 `Adaptive − baseline` Average Gain이다. 괄호는 strong-baseline family의 BH p다.

| Target | Random candidate | Round-robin | Dialogue follow-up | Controller-matched generic |
|---|---:|---:|---:|---:|
| Qwen3-1.7B | -0.0064 (.7487) | +0.0332 (.1448) | +0.0232 (.2023) | +0.0110 (.7487) |
| Qwen3-4B | +0.0161 (.8173) | +0.0656 (.0015) | +0.0629 (.0063) | +0.0470 (.0206) |
| Llama-3.2-3B | +0.0016 (.9946) | +0.0690 (.0015) | +0.0755 (.0015) | +0.0832 (.0002) |
| Gemma-3-4B | -0.0235 (.2898) | -0.0202 (.7487) | +0.0163 (.6936) | +0.0243 (.1395) |

Adaptive는 Qwen3-4B와 Llama에서 세 단순 follow-up baseline보다 높았다. 그러나 random candidate 대비 차이는 네 target 모두 유의하지 않았고, Qwen3-1.7B와 Gemma에서는 일부 baseline보다 평균이 낮았다. Candidate 생성 뒤 현재 score로 ranking하는 단계의 이득은 입증되지 않았다.

Direct generation, no coverage, no redundancy와 비교한 12개 macro test는 모두 BH p ≥ 0.333이었다. Coverage와 redundancy 항 각각의 기여도 확인되지 않았다. 이 결과는 ablation의 null result로 그대로 보고해야 한다.

## 외부 active 정보획득 baseline

Reviewer 2가 “where feasible” 요청한 active persona-inference/information-gain 비교를 위해 공개 코드를 그대로 재현한 것이 아니라 현재 protocol에 맞춘 `uncertainty_sampling` 기준선을 추가했다. Active-Prompt의 반복 확률 예측 엔트로피와 sequential active feature acquisition 원리를 사용한다. 각 1–4턴 뒤 공통 Qwen3-14B predictor가 대화만 보고 K=5 closed-set 예측을 만들며, 정규화 경험 엔트로피가 가장 큰 차원을 다음 간접 질문 대상으로 선택한다. 첫 질문·첫 응답은 기존 `dialogue_only` 행에서 정확히 재사용했고, 총 질문 수는 동일하게 5개다.

아래 값은 `Dialogue-only Adaptive − uncertainty_sampling` Average Gain이다. 네 target의 macro Wilcoxon은 모두 BH 보정 후 유의하지 않았고, 16개 차원별 McNemar 비교에도 BH p<.05가 없었다.

| Target | Δ Average Gain | paired-bootstrap 95% CI | BH p | + / − / tie |
|---|---:|---:|---:|---:|
| Qwen3-1.7B | +0.0072 | [-0.0261, +0.0409] | .7206 | 69 / 62 / 173 |
| Qwen3-4B | -0.0022 | [-0.0366, +0.0309] | .7206 | 70 / 67 / 167 |
| Llama-3.2-3B | -0.0264 | [-0.0654, +0.0118] | .5894 | 85 / 89 / 130 |
| Gemma-3-4B | -0.0394 | [-0.0756, -0.0036] | .2777 | 63 / 82 / 159 |

Gemma의 mean-difference bootstrap CI는 active 기준선 우세 방향이지만 Wilcoxon BH p=.2777이므로 일관된 유의 차이로 표현하지 않는다. `uncertainty_sampling − Original`은 Qwen3-4B +0.0815, Llama +0.1130, Gemma +0.0678로 CI가 0보다 높고 BH p<.001이었다. Qwen3-1.7B는 +0.0239이나 불확실했다. Random candidate 대비 네 target 모두 BH p≥.4402였으므로 엔트로피 기반 차원 선택의 추가 이득은 확인되지 않았다.

## 차원별 결과와 불확실성

신규 seed의 Adaptive vs Original에서 BH 보정 후 확인된 개선은 Qwen3-4B의 background(+0.0592)·interests(+0.0691), Llama의 background(+0.1283)·interests(+0.0757), Gemma의 background(+0.0625)였다. Qwen3-1.7B에는 유의한 차원이 없었다. 기존 seed에서는 Gemma interests가 음의 방향이었으므로 “모든 차원이 개선된다”는 주장을 사용할 수 없다.

세 seed 간 예측 불일치는 대부분 Adaptive와 Original 사이에 유의한 차이가 없었다. Gemma background만 Adaptive가 +0.1074 높았고 BH p=.0204였다. 즉 해당 조건에서는 Adaptive 예측의 seed 민감도가 더 컸다.

폐쇄형 label 밖 최종 예측도 별도 감사했다. 본 실험은 43,776개 prediction field 중 1,310개(2.99%)가 invalid였다. 방법별로 Original 2.45%, Adaptive 3.68%였으며 주로 interests에서 여러 label을 한꺼번에 출력한 경우였다. 점수 계산에서는 이런 출력이 오답으로 처리됐으며 사후 보정하지 않았다. 세-seed subset은 9,600개 field 중 370개(3.85%)가 invalid였다.

## Generation seed와 대체 backbone

100-persona subset의 세 seed 평균 Adaptive−Original 효과와 seed별 범위는 다음과 같다.

| Target | 3-seed 평균 | seed별 범위 | 양수 seed 수 |
|---|---:|---:|---:|
| Qwen3-1.7B | +0.0198 | [+0.0003, +0.0458] | 3/3 |
| Qwen3-4B | +0.0697 | [+0.0665, +0.0723] | 3/3 |
| Llama-3.2-3B | +0.0675 | [+0.0505, +0.0941] | 3/3 |
| Gemma-3-4B | +0.0243 | [+0.0122, +0.0312] | 3/3 |

방향은 모두 양수지만 seed별 bootstrap CI는 Qwen3-4B의 seed 20260913/20260914와 Llama의 seed 20260914만 0을 넘었다. 방향 안정성과 통계적 확실성을 구분해서 보고해야 한다.

Qwen3-1.7B target의 100-persona subset에서 Qwen3-14B PD-Agent 효과는 +0.0003 [-0.0620, +0.0649], Qwen3-8B는 -0.0035 [-0.0605, +0.0530]이었다. 효과 차이(8B−14B)는 -0.0038 [-0.0936, +0.0834], p=.9147이다. 대체 backbone에서 개선이 재현됐다고 할 수 없으며, backbone interaction도 검출되지 않았다.

## 실행 무결성과 비용

본 실험은 10,944/10,944행, robustness 신규 실험은 1,000/1,000행, 외부 active 기준선은 1,216/1,216행이 성공했다. 본 실험의 1,216개 target-persona 묶음마다 9개 방법이 모두 존재하며 첫 질문과 첫 응답이 정확히 동일했다. 외부 active 기준선도 기존 네 비교 방법과 304/304씩 같은 ground truth·첫 질문·첫 응답을 사용했다. 본 실험의 JSON parse fallback은 5건, robustness 신규 run은 1건, 외부 active 기준선은 0건이었다.

본 실험은 총 73,516,252 input tokens와 28,322,163 output tokens, 175,104개의 실제 model call을 사용했다. persona-method당 16 calls이다. 8개 H200 shard의 합은 3.119 H200 GPU-hours이고 가장 느린 shard는 1,548초였다. robustness 신규 run은 0.678 H200 GPU-hours였다. 외부 active 기준선은 19,929,164 input tokens, 4,359,337 output tokens, 43,776 calls로 persona당 36 calls였고 strict-paired 재실행의 incremental GPU 시간은 2.340 H200 GPU-hours, 최장 shard는 1,127초였다. 재사용한 첫 턴의 call/token은 비용 합계에 포함되지만 incremental GPU 시간에는 포함되지 않는다. 로컬 추론이라 API 요금은 없었고 전력 및 감가 비용은 측정하지 않았다.

실행 환경은 NVIDIA H200 143,771 MiB × 8, driver 580.126.16, vLLM 0.11.0, Transformers 4.57.6, PyTorch 2.8.0+cu126이다. 실제 temperature/top-p/max-token은 각 raw row의 per-call record가 기준이다. legacy top-level `decoding.json_calls.temperature`에는 note와 값이 불일치하므로 원고 표에는 per-call audit 값을 사용한다.

## 원고에서 사용할 수 있는 결론

고정된 5-turn 조건에서 대화형 적응 질문 수집은 Qwen3-4B와 Llama에서 Original 및 일부 단순 follow-up보다 개선됐다. 현재 candidate scoring/ranking은 random selection보다 안정적으로 좋지 않았고 coverage/redundancy ablation도 차이를 만들지 못했다. 따라서 기여는 “추가 대화형 elicitation의 조건부 효과”로 좁히고, scoring 구성요소의 우월성이나 모든 target·차원의 일반적 개선은 주장하지 않는 편이 결과와 맞다.

Qwen3-8B 실험은 backbone robustness를 지지하지 못했다. Graph는 사람 판정 전까지 `LLM-generated, exact-span-grounded intermediate representation`으로 기술해야 하며 `validated graph`라고 부르면 안 된다.

동일 closed-set schema와 target-response protocol에 바로 연결할 수 있는 공개 active persona-inference 구현은 확인되지 않았지만, 관련 연구 원리를 현재 protocol에 맞춘 외부 active 정보획득 기준선은 실행했다. 이는 공식 코드의 직접 재현이나 full expected-response information gain 구현이 아니라 최대 엔트로피 uncertainty-sampling adaptation으로 기술해야 한다. 결과상 Adaptive와 active 기준선의 차이는 확인되지 않았고, 둘 다 random-candidate보다 안정적으로 높지 않았다.

## 산출물

- 기존 paired 통계·schema·cost·정성 사례: `results/access_revision/existing_runs/`
- strong baseline/ablation 전체 결과: `results/access_revision/main/aggregate/`
- 세 seed 및 대체 backbone: `results/access_revision/robustness/aggregate/`
- 외부 active 정보획득 기준선: `results/access_revision/active_information_gain/main/aggregate/`
- active 기준선 설계·재현 절차: `docs/access_active_information_gain_baseline.md`
- prediction validity·환경·checkpoint·call 설정: `results/access_revision/audit/`
- graph annotation pack: `results/access_revision/graph_validity/annotation_sample.csv`
- annotator guideline: `docs/access_graph_annotation_guideline.md`
- 전체 실험 계획: `docs/access_revision_experiment_plan.md`
- 리뷰어별 코멘트·대응·완료 현황: `docs/access_reviewer_comment_response_status.md`

두 annotator가 CSV의 `a_*`, `b_*` 열을 독립 작성하고 adjudication을 마치면 다음 명령으로 agreement와 relation별 validity를 계산할 수 있다.

```bash
/opt/conda/envs/tracecal_rl/bin/python -m evaluation.score_graph_validity_audit \
  results/access_revision/graph_validity/annotation_sample.csv \
  --output results/access_revision/graph_validity/validity_report.json
```
