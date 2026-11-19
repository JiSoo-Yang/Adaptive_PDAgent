# Qualitative cases across all revision baselines

상태: **DATA_READY / MANUSCRIPT_EDIT_ONLY**. 새 inference나 rerun 없이 완료 로그에서 추출했다.

## Case selection

Revision seed `20260913`에서 target별 persona-level `Dialogue-only Adaptive − Original` Average Gain이 최대인 성공 사례 하나와 최소인 실패 사례 하나를 선택했다.

| Target | Case | Persona index | Adaptive−Original Average Gain |
|---|---|---:|---:|
| Qwen3-1.7B | Success | 116 | +1.3048 |
| Qwen3-1.7B | Failure | 69 | −0.8870 |
| Qwen3-4B | Success | 303 | +1.2325 |
| Qwen3-4B | Failure | 34 | −0.8962 |
| Llama-3.2-3B | Success | 232 | +1.2325 |
| Llama-3.2-3B | Failure | 5 | −1.2956 |
| Gemma-3-4B | Success | 208 | +1.2325 |
| Gemma-3-4B | Failure | 297 | −1.2956 |

정확한 persona ID와 full-precision difference는 `qualitative_cases_index.csv`에 있다.

## 추출된 10개 arm

각 사례에 다음 method가 모두 존재한다.

1. Original
2. Dialogue-only Adaptive
3. Random candidate
4. Round robin
5. Dialogue follow-up
6. Controller-matched generic
7. Direct generation ablation
8. No-coverage ablation
9. No-redundancy ablation
10. Adapted active uncertainty sampling

각 arm에는 다음을 보존했다.

- five questions와 Target responses
- observable decision JSON과 `rationale_summary`
- evidence state
- uncertainty scores/selected dimension, 해당 method에서 존재할 때
- graph-update summary와 final grounded graph
- final prediction과 parse status
- dimension raw scores, normalized gains, Average Gain
- source raw file, seed, prompt/config version

Full cases: `qualitative_cases_all_methods.jsonl`.

## “추론”의 범위

Runner prompt는 chain-of-thought를 제공하지 말도록 명시했고 hidden reasoning을 저장하지 않았다. 따라서 hidden chain-of-thought는 **`[MISSING]`**이며 기존 로그에서 복구할 수 없다. JSONL의 “inference trace”는 공개 가능한 operational trace, 즉 decision metadata, 짧은 rationale summary, evidence state, entropy score와 graph update다.

이를 얻기 위해 rerun할 필요는 없고, 원고에는 hidden reasoning 대신 이 observable trace를 제시해야 한다.

## Pairing과 rerun 여부

- 8 cases × 10 arms = 80개 arm이 모두 완료 로그에 존재한다.
- 같은 case 안의 persona, ground truth, 최초 question/response는 exact-paired다.
- Reviewer가 열거한 4개 strong baseline과 active baseline을 모두 포함했다.
- Rerun required: `False`.

`full_gai`와 `selective_gai`는 Reviewer 2가 요청한 strong baseline family가 아니며, 현재 `20260913` main run에는 없다. 이 둘의 기존 결과는 `20260831` source run에 있어 최초 response realization이 다르므로 10-arm case에 혼합하지 않았다. 이 두 graph variant까지 **동일 `20260913` transcript realization**으로 추가하는 자료는 `[MISSING]`이고 rerun이 필요하지만, 현재 요청의 baseline 범위를 충족하는 데에는 필요하지 않다.

기존 `20260831` Original/Adaptive 8개 사례는 `results/access_revision/existing_runs/qualitative_pairs.jsonl`에 그대로 유지했다.

## 원고 배치

본문에는 target별 성공/실패 중 대표 2–4개만 간결히 싣고, 80-arm trace는 Supplementary Data로 연결하는 편이 읽기 쉽다. 사례 선택이 extreme-case sampling임을 명시하고 평균적 행동을 대표한다고 주장하지 않아야 한다.

