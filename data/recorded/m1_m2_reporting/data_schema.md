# Raw CSV and data schema

## Source of truth

| File | Role |
|---|---|
| `results/selective_gai/raw_runs.jsonl` | 완료된 4,864개 target-method-persona run의 원자료 |
| `results/selective_gai/heldout_personas.jsonl` | 304개 frozen persona와 ground truth |
| `results/selective_gai/persona_manifest.json` | cohort seed, N, persona file SHA-256 |
| `evaluation/metrics.py` | dimension score와 cohort metric 구현 |
| `evaluation/aggregate_table3_table4.py` | majority gain, bootstrap, Wilcoxon, BH 구현 |
| `evaluation/analyze_access_revision.py` | M1 contrast, test family, seed 배정 구현 |
| `evaluation/build_m1_m2_reporting.py` | 이 폴더의 CSV 재생성 및 audit 구현 |

입력과 생성 CSV의 SHA-256은 `manifest.json`에 보존했다.

## `M1_M2_raw_results.csv`

- Rows: 9,728 = 4 targets × 304 personas × 2 methods × 4 dimensions
- Primary key: `(target_model, persona_id, method, dimension)`
- 요청된 long-format field인 `target_model`, `persona_id`, `method`, `dimension`, `raw_score`, `majority_baseline`, `normalized_gain`, `average_gain`, `original_average_gain`, `adaptive_average_gain`, `difference`를 모두 포함한다.
- `method`은 `original` 또는 `adaptive`이며, `difference`는 각 행에서 동일 persona의 `adaptive_average_gain - original_average_gain`이다.
- Pairing audit에 필요한 `persona_index`, `cohort_seed`, `run_base_seed`, 최초 question/answer hash도 보조 열로 포함한다.
- `raw_score`는 현재 각 persona-dimension에서 0/1이다. Cohort-level micro-F1을 persona별로 복제한 값이 아니다.

## `m1_persona_level.csv`

- Rows: 1,216 = 4 targets × 304 personas
- Primary key: `(target_model, persona_index)`
- 한 행이 M1 Wilcoxon의 후보 관측값 하나이며 `difference_adaptive_minus_original`이 실제 입력값이다.

| Field/pattern | Type | Meaning |
|---|---|---|
| `target_model` | string | target checkpoint 이름 |
| `persona_index` | integer | frozen cohort index, 0–303 |
| `persona_id` | string | canonical ground-truth SHA-256 기반 ID |
| `cohort_seed` | integer | persona sampling seed, 20260802 |
| `sampling_nonce` | integer | duplicate rejection nonce; 현재 전부 0 |
| `run_base_seed` | integer | held-out execution base seed, 20260831 |
| `initial_question_sha256` | string | 최초 질문 문자열의 SHA-256 |
| `initial_answer_sha256` | string | 최초 응답 문자열의 SHA-256 |
| `majority_baseline_{dimension}` | float | held-out 304명에서 구한 dimension baseline |
| `{original,adaptive}_{dimension}_score` | float | persona-level score; 현재 0/1 |
| `{original,adaptive}_{dimension}_gain` | float | `(score−baseline)/(1−baseline)` |
| `{original,adaptive}_average_gain` | float | 네 dimension gain의 동일 가중 평균 |
| `difference_adaptive_minus_original` | float | Adaptive Average Gain − Original Average Gain |
| `difference_sign` | enum | `positive`, `negative`, `tie` |

`dimension`은 `social_role`, `personality`, `background`, `interests` 중 하나다.

## `m1_primary_summary.csv`

- Rows: 4, target당 하나
- Primary key: `target_model`

주요 필드:

- 표본과 방향: `n_total_pairs`, `n_nonzero_wilcoxon`, `positive_pairs`, `negative_pairs`, `tied_pairs`
- 기술통계: 두 method의 mean Average Gain, mean difference
- Wilcoxon: statistic, W+/W−, raw p, zero method, alternative, continuity correction, requested/resolved method, SciPy version
- Bootstrap: repetitions, seed, CI method, lower/upper bound
- Multiple testing: BH family, family size, adjusted p
- 효과크기: nonzero absolute ranks의 rank-biserial effect

## `dimension_level_tests.csv`

- Rows: 16 = 4 targets × 4 dimensions
- Primary key: `(target_model, dimension)`

| Field | Meaning |
|---|---|
| `original_correct_count`, `adaptive_correct_count` | 304명 중 correct 수 |
| `original_accuracy`, `adaptive_accuracy` | correct count / 304 |
| `both_correct`, `both_incorrect` | concordant pair 수 |
| `b_original_correct_adaptive_incorrect` | Adaptive loss discordance |
| `c_original_incorrect_adaptive_correct` | Adaptive gain discordance |
| `mcnemar_p_raw` | exact two-sided binomial p-value |
| `ci95_*` | raw accuracy difference의 paired percentile bootstrap CI |
| `p_bh` | 16-test family의 BH-adjusted p-value |
| `dimension_level_wilcoxon` | 완료 분석에서 미수행했음을 명시 |

## `pairing_sampling_audit.csv`

- Rows: 16 = 4 targets × 4 source methods
- Primary key: `(target_model, method)`
- cell별 final count, unique/missing/duplicate index, 성공 여부와 네 method 간 persona·ground truth·최초 문답 exact pairing을 기록한다.

## `majority_baselines.csv`

- Rows: 4 dimensions
- `majority_rule`은 social role의 global coarse category 또는 나머지 dimension의 trait/category-conditional label map을 JSON string으로 저장한다.

## 재현과 무결성 검사

저장소 root에서 실행한다.

```bash
/opt/conda/envs/tracecal_rl/bin/python -m evaluation.build_m1_m2_reporting
```

스크립트는 다음 invariant가 깨지면 실패한다.

- 304 persona와 연속 index `0…303`
- 4 targets × 4 source methods × 304 unique raw keys
- Original/Adaptive의 persona ID 일치
- M1에 사용한 dimension score가 모두 binary
- 재구성한 Wilcoxon `min(W+, W−)`와 SciPy 반환 statistic 일치

모델 inference는 수행하지 않는다.

