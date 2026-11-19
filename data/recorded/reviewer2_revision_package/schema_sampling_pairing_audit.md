# Schema, sampling, and pairing audit

상태: **DATA_READY / MANUSCRIPT_EDIT_ONLY**. 추가 모델 실험은 필요 없다. Cross-dimension semantic contradiction filter는 구현돼 있지 않으므로 그 부분은 아래에 `[MISSING]`으로 표시한다.

## 전체 schema와 sampling probability

전체 157개 category/value 행, 이론 sampling probability, development/held-out 빈도는 `sampling_probabilities_and_frequencies.csv`에 있다. Canonical label text의 원본은 `schema/persona_schema.json`, label-space와 held-out frequency의 기존 감사본은 `results/access_revision/existing_runs/schema_and_sampling.json`이다.

Sampling은 hierarchical uniform이다. Category를 먼저 균등 추출하고 해당 category 안의 value를 균등 추출하므로, 모든 specific label 또는 전체 persona 조합이 같은 확률을 갖지는 않는다.

| Dimension | Category 수 | Value space | Category 확률 | 특정 value의 joint 확률 |
|---|---:|---|---:|---:|
| Social role | 3 coarse categories | 43 occupations; category별 14, 14, 15개 | 1/3 | category 크기 14이면 1/42, 크기 15이면 1/45 |
| Personality | 5 Big-Five traits | trait마다 yes/no | 1/5 | 1/10 |
| Background | 5 categories | education 6, location 4, family status 5, economic status 5, work experience 5 | 1/5 | 각각 1/30, 1/20, 1/25, 1/25, 1/25 |
| Interests | 7 categories | hobbies 13, content preferences 10, technology adoption 5, shopping style 7, communication style 8, values 14, social-media usage 2 | 1/7 | 각각 1/91, 1/70, 1/35, 1/49, 1/56, 1/98, 1/14 |

### Development/held-out category frequency

| Dimension | Category/trait | Development N=100 | Held-out N=304 |
|---|---|---:|---:|
| Social role | general role | 32 | 97 |
| Social role | professional | 32 | 118 |
| Social role | technical/management | 36 | 89 |
| Personality | openness | 10 | 62 |
| Personality | conscientiousness | 25 | 53 |
| Personality | extroversion | 21 | 58 |
| Personality | agreeableness | 17 | 70 |
| Personality | neuroticism | 27 | 61 |
| Background | economic status | 25 | 67 |
| Background | education | 13 | 48 |
| Background | family status | 17 | 48 |
| Background | location | 19 | 66 |
| Background | work experience | 26 | 75 |
| Interests | communication style | 19 | 41 |
| Interests | content preferences | 10 | 37 |
| Interests | hobbies | 10 | 38 |
| Interests | shopping style | 16 | 46 |
| Interests | social-media usage | 13 | 43 |
| Interests | technology adoption | 15 | 52 |
| Interests | values | 17 | 47 |

Value별 빈도는 157행 CSV에 모두 포함했다.

## Valid persona combination 생성 규칙

한 persona는 다음 네 항목의 Cartesian product로 만든다.

1. 한 social-role category와 그 안의 occupation 하나
2. 한 Big-Five trait와 polarity `yes`/`no` 하나
3. 한 background category와 그 안의 value 하나
4. 한 interest category와 그 안의 value 하나

Schema상 가능한 raw combination 수는 `43 × 10 × 25 × 59 = 634,250`이다. 각 index의 random generator는 `random.Random(f"{base_seed}:{index}:{nonce}")`이고 네 dimension은 독립적으로 뽑는다.

Cross-dimension plausibility 또는 contradiction constraint: **`[MISSING]`**. 코드와 schema에는 occupation, background, interest 사이의 의미적 모순을 금지하는 규칙이 없다. 원고에는 “No additional cross-dimension plausibility constraints were encoded”라고 밝혀야 하며, “all sampled personas are semantically coherent”라고 주장하면 안 된다.

## Unique/replacement sampling

- Development: 100명, seed `20260801`
- Previously observed Table 3 cohort: 304명, seed `20260730`
- Frozen held-out: 304명, seed `20260802`
- 세 cohort 간 persona ID 및 canonical ground-truth overlap: 0
- Held-out final unique persona IDs: 304/304
- Held-out sampling nonce: 모두 0; 실제 duplicate draw 0
- 구현은 duplicate persona ID를 만나면 nonce를 높여 다시 뽑으므로 final cohort는 persona identity 기준 without replacement다.
- 분석에서 제외한 held-out persona: 없음

## Pairing audit

### M1 source run, seed 20260831

`original`, `dialogue_only`, `full_gai`, `selective_gai` 네 method는 모든 target에서 각각 304개를 갖는다. `results/access_revision/m1_m2_reporting/pairing_sampling_audit.csv`에서 다음이 모두 True다.

- 같은 persona ID와 ground truth
- 같은 최초 질문 문자열
- 같은 최초 Target response 문자열
- 같은 frozen persona input SHA-256
- 누락, duplicate, failed row 없음

### Revision baseline/ablation run, seed 20260913

`revision_methods_pairing_audit.csv`는 다음 10개 method를 함께 검사한다.

`original`, `dialogue_only`, `random_candidate`, `round_robin`, `dialogue_followup`, `controller_matched_generic`, `adaptive_direct`, `adaptive_no_coverage`, `adaptive_no_redundancy`, `uncertainty_sampling`.

네 target 모두 304/304 persona에서 10개 method가 존재하며 persona ID, ground truth, 최초 질문, 최초 response가 exact match다. 모든 row가 성공했고 제외 persona는 없다.

## 원고 반영 문장

> We sampled personas hierarchically by first choosing a category uniformly and then choosing a value uniformly within that category. The four persona dimensions were sampled independently; no additional cross-dimension plausibility constraints were encoded. Duplicate persona identities would have been rejected, although all 304 held-out personas were unique on their first draw. Development and held-out cohorts used seeds 20260801 and 20260802 and had zero persona overlap.

> All paired methods used exactly the same persona ID, ground truth, first-question string, and first-response realization for each target-persona pair. Every target-method cell contained all 304 held-out personas, with no failed, duplicate, missing, or excluded indices.

