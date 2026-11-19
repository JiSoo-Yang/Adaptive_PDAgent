# Implementation protocol report

상태: **DATA_READY / MANUSCRIPT_EDIT_ONLY**. 실행 prompt와 per-call 설정은 raw JSONL에 보존되어 있다. 이 보고서는 코드를 운영 정의로 삼으며 새 실험을 수행하지 않았다.

## 구현 source

| 범위 | 파일/함수 |
|---|---|
| Main runner와 모든 prompt | `evaluation/run_table3_table4_vllm.py` |
| Method registry, graph validation, fallback questions, decision parsing | `evaluation/table3_table4.py` |
| Selective GAI gate, utility weights, stop rule | `evaluation/selective_gai.py` |
| 9-method revision launcher | `evaluation/run_access_revision_8gpu.sh` |
| Active baseline launcher | `evaluation/run_access_active_baseline_8gpu.sh` |
| Frozen selective configuration | `results/selective_gai/frozen_config.yaml` |
| 실제 observed calls/decoding | `results/access_revision/audit/observed_call_settings.csv` |
| Raw main prompts and outputs | `results/access_revision/main/raw/*/*.jsonl` |
| Raw active prompts and outputs | `results/access_revision/active_information_gain/main/raw/*/*.jsonl` |

## 공통 interaction protocol

- Hidden persona는 Target LLM의 system prompt에만 전달된다. Target은 label을 직접 말하지 않고 자연스러운 한 문장으로 답하도록 지시받는다.
- 첫 질문은 ordinary activities의 구체적 설명을 유도하는 공통 open-ended question prompt로 생성된다.
- Paired conditions는 동일 prompt만 공유한 것이 아니라 최초 question/response 문자열을 exact reuse한다.
- 최대 budget은 5 turns다.
- Target response: temperature 0.7, top-p 0.8, max new tokens 256.
- Question/action generation: temperature 0.7, top-p 0.8. Role별 max tokens는 `observed_call_settings.csv`에 있다.
- Graph extraction 및 final prediction: temperature 0.0, top-p 0.8. Graph extraction max 768 tokens, final prediction max 384 tokens.
- Common PD-Agent/final predictor는 Qwen3-14B revision `40c069824f4251a91eefaf281ebe4c544efd3e18`이다.

## Question-generation policy

### Original PD-Agent

Dialogue history만 보고 일반 open-ended follow-up 하나를 생성한다. Evidence state, target dimension, early stop, candidate label을 사용하지 않는다. 항상 5 turns다.

### Dialogue-only Adaptive

Visible dialogue만 사용한다. 한 JSON call에서 아직 부족하거나 ambiguous한 정보를 판단하고 정확히 3개 indirect candidate question을 생성한 뒤 하나를 선택한다. Candidate schema에는 `coverage_gain`과 `redundancy_penalty`가 있고, 모든 dimension이 충분히 지지될 때만 `Stop`을 허용한다. Graph node/edge/novelty는 controller 입력에 넣지 않는다.

실제 host code의 한계도 명시해야 한다.

- Candidate score의 강제 numeric range: **`[MISSING]`**
- Coverage/redundancy의 deterministic weight 또는 합산 공식: **`[MISSING]`**
- Candidate score의 host-side recomputation 또는 validation: **`[MISSING]`**
- 동률 candidate의 deterministic tie-break: **`[MISSING]`**

즉, 이 policy는 학습되거나 수식으로 최적화된 acquisition model이 아니라 Qwen3-14B가 prompt 안에서 candidate를 생성·평가·선택하는 **LLM-prompted controller**다. 원고의 Equation (7)이 deterministic implemented score처럼 쓰여 있다면 prompt-level heuristic로 고쳐야 한다.

### Strong baselines

- `random_candidate`: Adaptive와 같은 3개 candidate를 생성한 뒤 candidate score를 무시하고 `stable_seed % candidate_count`로 하나를 선택한다.
- `round_robin`: 질문 2–5를 social role, personality, background, interests 순서로 한 번씩 target한다. 현재 ambiguity/coverage를 평가하지 않는다.
- `dialogue_followup`: 가장 최근 응답에 specific natural follow-up 하나를 생성하며 target dimension, candidates, ambiguity/coverage score를 사용하지 않는다.
- `controller_matched_generic`: Adaptive와 같은 3-candidate JSON interaction shape를 사용하지만 conversational specificity와 repetition만 평가하고 persona ambiguity, coverage, target dimension은 사용하지 않는다.

### Controller ablations

- `adaptive_direct`: least-supported dimension을 찾은 뒤 candidate 생성·ranking·coverage/redundancy score 없이 질문 하나를 직접 생성한다.
- `adaptive_no_coverage`: 3개 candidate 중 redundancy만 사용하며 expected coverage gain을 사용하지 않는다.
- `adaptive_no_redundancy`: 3개 candidate 중 expected coverage만 사용하며 redundancy를 사용하지 않는다.

## Coverage와 redundancy 제어

Dialogue-only Adaptive와 세 ablation의 coverage/redundancy는 prompt에 나타나는 LLM judgment다. Main Adaptive에는 별도의 deterministic evidence-count coverage threshold나 redundancy formula가 없다.

Selective graph-guided variant에는 별도 deterministic 제어가 있다.

- Dimension confidence: `min(1, 0.25×concept_count + 0.15×edge_count + 0.10×min(span_count,2))`
- Frozen coverage threshold: 0.35
- Frozen novelty/stagnation threshold: 0.10
- Utility: `0.30 coverage + 0.25 discrimination + 0.25 novelty − 0.15 redundancy − 0.05 leakage`
- 모든 utility field는 0–1로 clamp한다.
- Graph candidate가 actionable gate를 통과하고 dialogue utility보다 frozen margin 0.00 이상일 때 graph source를 선택한다. 아니면 dialogue fallback이다.

이 Selective GAI 수식을 Dialogue-only Adaptive의 구현식으로 혼동하면 안 된다.

## Parsing, fallback, and tie-break

- JSON parser는 응답의 마지막 balanced JSON object를 읽는다.
- Invalid/missing action은 `Explore`, invalid target dimension은 `null`, non-list candidates는 empty list로 바꾼다.
- 생성 question을 정리한 뒤 empty, schema-label leakage, 금지된 meta term이 있으면 dimension별 deterministic fallback bank를 turn index로 선택한다.
- Random candidate는 stable seed 기반 index로 재현된다. Candidate가 없으면 parsed selected question을 유지하고, 이것도 invalid하면 공통 fallback question을 사용한다.
- Active uncertainty baseline tie-break는 normalized entropy 최대, 그다음 least-asked dimension, 마지막으로 fixed order `social_role`, `personality`, `background`, `interests`다.
- Dialogue-only Adaptive candidate 동률의 host-side tie-break는 `[MISSING]`; LLM selected output을 그대로 사용한다.

## Stopping rule

- Original과 네 strong baseline, active uncertainty baseline: stopping disabled, 5 turns 고정.
- Dialogue-only Adaptive와 세 dialogue ablation: LLM이 visible dialogue가 네 dimension을 모두 지지한다고 판단할 때 `Stop`을 출력할 수 있다. Numeric threshold는 `[MISSING]`.
- 실제 304-persona held-out M1과 `20260913` main revision run에서 Adaptive는 모든 case에 5 turns를 사용했다. 실질적인 early stopping 효과는 관측되지 않았다.
- Selective GAI: minimum turn 3, all-covered/no-competition이면 stop. 또는 2-turn stagnation, no valid competition, no actionable gap, expected gain < 0.25 조건에서 stop한다. 이 설정은 held-out 확인 전에 development에서 freeze됐다.

## Final scoring

Final predictor는 interview와 해당 run의 grounded graph를 받고 closed-set JSON을 생성한다. Scoring, fuzzy canonicalization, majority baseline, normalized gain과 통계는 다음에 구현돼 있다.

- `evaluation/metrics.py`
- `evaluation/aggregate_table3_table4.py`
- `evaluation/analyze_access_revision.py`
- `results/access_revision/m1_m2_reporting/m2_metric_aggregation_and_analysis_unit.md`

## 원고 claim 제한

> The Adaptive controller is an LLM-prompted, dialogue-conditioned heuristic that jointly generates, scores, and selects candidate questions. The current implementation does not enforce a deterministic weighted acquisition objective or a host-side tie-break among equally scored candidates.

이 문구를 사용하면 구현에 없는 learned/optimized acquisition model이나 deterministic score를 주장하는 문제를 피할 수 있다.

