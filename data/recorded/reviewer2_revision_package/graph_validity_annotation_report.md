# Graph validity annotation report

상태: **ADDITIONAL_ANNOTATION_REQUIRED / PENDING**. Annotation pack과 scoring code는 준비됐지만 사람 판정 결과는 없다.

## 준비된 140-edge pack

- File: `results/access_revision/graph_validity/annotation_sample.csv`
- Sampling manifest: `results/access_revision/graph_validity/manifest.json`
- Guideline: `docs/access_graph_annotation_guideline.md`
- Scoring code: `evaluation/score_graph_validity_audit.py`
- Source run: `results/selective_gai/raw_runs.jsonl`
- Annotation sample seed: `20260913`

| Relation type | Available source edges | Sampled |
|---|---:|---:|
| part-of | 3,489 | 20 |
| member-of | 450 | 20 |
| instrument | 2,617 | 20 |
| theme | 4,057 | 20 |
| cause-of | 5,528 | 20 |
| in | 1,638 | 20 |
| temporal | 562 | 20 |
| Total | — | 140 |

각 행은 question, response, source/target concept, assigned relation, supporting span을 포함한다. Annotator는 hidden persona와 상대 annotator label을 보지 않고 다음 세 항목을 `yes/no/uncertain`으로 판정하게 설계됐다.

1. source/target concepts validity
2. assigned semantic relation validity
3. supporting span이 해당 triple을 지지하는지

## 현재 annotation 상태

| Required output | Current state |
|---|---|
| Annotator A 3개 판단 × 140행 | `[MISSING]`; 420 cells empty |
| Annotator B 3개 판단 × 140행 | `[MISSING]`; 420 cells empty |
| Annotator A notes | optional, 현재 empty |
| Annotator B notes | optional, 현재 empty |
| Raw agreement 3종 | `[MISSING]`; 두 독립 annotation 필요 |
| Cohen's kappa 3종 | `[MISSING]`; 두 독립 annotation 필요 |
| Adjudicated relation-valid labels | `[MISSING]`; 140 cells empty |
| Overall adjudicated validity | `[MISSING]` |
| Relation별 adjudicated validity | `[MISSING]` |

빈 annotation CSV에 scoring script를 실행하면 invalid/unfilled label error가 발생하는 것이 정상이다.

완료 후 명령:

```bash
/opt/conda/envs/tracecal_rl/bin/python \
  evaluation/score_graph_validity_audit.py \
  results/access_revision/graph_validity/annotation_sample.csv \
  --output results/access_revision/graph_validity/scored_report.json
```

## 필요한 human action

1. Annotator A와 B가 독립적으로 140행을 판정한다.
2. 두 pass가 끝난 뒤 disagreement를 adjudicate한다.
3. Scoring script로 raw agreement, Cohen's kappa, relation별 validity를 계산한다.
4. 원고와 response에 annotator 자격/교육, blind 절차, adjudicator, 결과를 추가한다. 이 메타데이터도 현재 `[MISSING]`이다.

## 완료 전 graph claim 제한

사용 가능한 표현:

> We use an LLM-generated intermediate graph whose nodes and edges are constrained to exact supporting spans in the dialogue. Exact-span validation establishes textual grounding but does not by itself establish semantic relation validity.

피해야 할 표현:

- validated bridging-inference structure
- semantically correct relation graph
- expert-verified graph
- graph relation accuracy가 입증됐다는 주장

Response letter에는 annotation 결과를 제출 전에 채우거나, 끝내지 못할 경우 graph를 `LLM-generated, exact-span-grounded intermediate representation`으로 제한했다는 수정 조치를 명시해야 한다.

