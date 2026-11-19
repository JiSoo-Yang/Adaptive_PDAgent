# Pairing and sampling audit

## 감사 범위

- 원자료: `results/selective_gai/raw_runs.jsonl`
- frozen persona manifest: `results/selective_gai/heldout_personas.jsonl`
- target: 4개
- source methods: `original`, `dialogue_only`, `full_gai`, `selective_gai`
- M1 직접 contrast: `dialogue_only − original`

## Method별 최종 평가 수

| Target | Original | Dialogue-only Adaptive | Full GAI | Selective GAI |
|---|---:|---:|---:|---:|
| Qwen3-1.7B | 304 | 304 | 304 | 304 |
| Qwen3-4B | 304 | 304 | 304 | 304 |
| Llama-3.2-3B-Instruct | 304 | 304 | 304 | 304 |
| Gemma-3-4B-IT | 304 | 304 | 304 | 304 |
| Method total | 1,216 | 1,216 | 1,216 | 1,216 |

총 4,864행 모두 `success=true`다. 각 target-method cell에서 persona index는 정확히 `0…303`이고 duplicate index, missing index, 분석 제외 persona는 없다.

## Pairing 결과

네 target 각각의 304개 persona bundle에서 다음 조건을 원자료로 직접 확인했다.

| Audit item | Qwen3-1.7B | Qwen3-4B | Llama-3.2-3B | Gemma-3-4B |
|---|---:|---:|---:|---:|
| 네 source method 모두 존재 | True | True | True | True |
| persona ID가 method 간 동일 | True | True | True | True |
| ground truth가 method 간 동일 | True | True | True | True |
| 최초 질문 문자열이 method 간 동일 | True | True | True | True |
| 최초 응답 문자열이 method 간 동일 | True | True | True | True |
| frozen manifest의 persona와 동일 | True | True | True | True |
| raw row의 persona-input SHA-256이 manifest와 동일 | True | True | True | True |

“같은 prompt를 사용했다”는 수준이 아니라, method별 저장 row의 `turn_records[0].question`과 `turn_records[0].answer` 문자열이 target-persona bundle 안에서 exact equality를 만족한다. 이후 질문과 응답은 method policy에 따라 달라질 수 있다.

## Sampling 방식

- Held-out cohort seed: `20260802`
- 크기: 304
- final unique persona IDs: 304
- final sampling: persona identity 기준 without replacement
- 구현: 각 index에 대해 `random.Random(f"{base_seed}:{index}:{nonce}")`를 사용해 schema component를 독립적으로 선택하고, 이전 persona와 같은 `persona_id`가 나오면 nonce를 증가시켜 다시 뽑는다.
- 실제 held-out cohort의 `sampling_nonce`: 전부 0
- 실제 duplicate rejection 횟수: 0
- 제외 persona: 없음

따라서 이 cohort는 코드상 duplicate-rejection으로 최종 uniqueness를 보장하고, 실제 seed `20260802`에서는 첫 draw 304개가 모두 고유했다. Replacement로 같은 persona를 여러 평가 행에 반복한 표본이 아니다.

## Seed와 data split

| 용도 | N | Seed | held-out와의 관계 |
|---|---:|---:|---|
| Development cohort | 100 | 20260801 | 별도 sampling; ID 및 canonical persona overlap 0 |
| Previously observed Table 3 cohort | 304 | 20260730 | 별도 sampling; ID 및 canonical persona overlap 0 |
| Frozen held-out cohort | 304 | 20260802 | M1/M2 분석 cohort |
| Held-out model-run base seed | — | 20260831 | M1 원자료의 모든 Original/Adaptive row에 저장 |

`frozen_config.yaml`에는 held-out cohort가 결과 확인 전에 `status: not_observed_at_freeze`로 기록되어 있다. Development, previously observed, frozen held-out 세 cohort 사이의 persona-ID와 canonical-persona overlap은 모두 0이라고 `development_summary.md`에 기록되어 있다.

각 LLM call의 세부 seed도 원 JSONL의 `target_call`, `question_call`, `final_prediction_call` 등에 저장되어 있다. 하나의 고정 call seed를 모든 persona에 반복 적용한 방식은 아니며, 재현 audit에서 공통 run-level seed는 `base_seed=20260831`이다.

## 분석 제외와 실패 처리

- M1 Original/Adaptive 2,432행: 모두 성공, final prediction parse 성공, 제외 0
- 전체 네 source method 4,864행: 모두 성공, 누락 0
- 사후 complete-case 삭제, outlier 삭제, tie 삭제를 통한 persona 제외는 없음
- Wilcoxon의 zero difference는 통계량의 rank 계산에서만 빠지며 원 관측값과 `N=304`에서 삭제되지 않는다.

행별 감사 결과는 `pairing_sampling_audit.csv`, sampling nonce와 SHA-256은 `manifest.json`에 있다.

