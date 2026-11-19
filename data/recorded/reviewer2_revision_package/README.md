# Reviewer 2 M1–M12, m1–m9 revision package

기준일: 2026-09-15. 새 model inference를 수행하지 않고 기존 실험·분석·로그·코드에서 추출했다. 확인할 수 없는 값은 `[MISSING]`으로 표시했다.

## 13개 요청 산출물

| No. | 산출물 | 실제 파일 | 상태 |
|---:|---|---|---|
| 1 | manuscript_source_and_mapping | [`manuscript_source_and_mapping.md`](manuscript_source_and_mapping.md) | **PARTIAL**; 편집 가능한 최신 manuscript/`.bib` `[MISSING]` |
| 2 | M1_M2_statistics_report | 기존 [`m1_primary_statistical_analysis_full_report.md`](../m1_m2_reporting/m1_primary_statistical_analysis_full_report.md), [`m2_metric_aggregation_and_analysis_unit.md`](../m1_m2_reporting/m2_metric_aggregation_and_analysis_unit.md), [`dimension_level_statistical_test_report.md`](../m1_m2_reporting/dimension_level_statistical_test_report.md) | **DATA_READY / MANUSCRIPT_EDIT_ONLY** |
| 3 | M1_M2_raw_results.csv | 기존 [`M1_M2_raw_results.csv`](../m1_m2_reporting/M1_M2_raw_results.csv), schema는 [`data_schema.md`](../m1_m2_reporting/data_schema.md) | **DATA_READY**; 9,728 long rows |
| 4 | schema_sampling_pairing_audit | [`schema_sampling_pairing_audit.md`](schema_sampling_pairing_audit.md), [`sampling_probabilities_and_frequencies.csv`](sampling_probabilities_and_frequencies.csv), [`revision_methods_pairing_audit.csv`](revision_methods_pairing_audit.csv) | **DATA_READY / MANUSCRIPT_EDIT_ONLY** |
| 5 | implementation_protocol_report | [`implementation_protocol_report.md`](implementation_protocol_report.md) | **PARTIAL**; 실행 protocol은 추출됐으나 claimed numeric candidate weights/threshold/tie-break 중 구현에 없는 값은 `[MISSING]` |
| 6 | robustness_results_report | 기존 [`robustness/aggregate/report.md`](../robustness/aggregate/report.md), [`seed_effects.csv`](../robustness/aggregate/seed_effects.csv), [`backbone_robustness.csv`](../robustness/aggregate/backbone_robustness.csv) | **DATA_READY / MANUSCRIPT_EDIT_ONLY**; 비재현 결과 포함 |
| 7 | baseline_comparison_report | [`baseline_comparison_report.md`](baseline_comparison_report.md) | **DATA_READY / MANUSCRIPT_EDIT_ONLY**; external method는 protocol adaptation, direct official reproduction은 `[MISSING]` |
| 8 | tradeoff_prediction_ablation_report | [`tradeoff_prediction_ablation_report.md`](tradeoff_prediction_ablation_report.md), [`budget_allocation.csv`](budget_allocation.csv) | **DATA_READY / MANUSCRIPT_EDIT_ONLY**; validity/allocation inferential CI는 `[MISSING]` |
| 9 | graph_validity_annotation_report | [`graph_validity_annotation_report.md`](graph_validity_annotation_report.md), 기존 [`annotation_sample.csv`](../graph_validity/annotation_sample.csv) | **ADDITIONAL_ANNOTATION_REQUIRED / PENDING** |
| 10 | qualitative_cases_all_methods | [`qualitative_cases_all_methods.md`](qualitative_cases_all_methods.md), [`qualitative_cases_index.csv`](qualitative_cases_index.csv), [`qualitative_cases_all_methods.jsonl`](qualitative_cases_all_methods.jsonl) | **DATA_READY / MANUSCRIPT_EDIT_ONLY**; 8 cases×10 arms, rerun 불필요 |
| 11 | cost_audit_report | [`cost_audit_report.md`](cost_audit_report.md) | **PARTIAL / MANUSCRIPT_EDIT_ONLY**; power/depreciation/utilization/cached-token split `[MISSING]` |
| 12 | prior_work_and_release_audit | [`prior_work_and_release_audit.md`](prior_work_and_release_audit.md) | **PARTIAL / MANUSCRIPT_EDIT + EXTERNAL ACTION REQUIRED** |
| 13 | final_table_figure_audit | [`final_table_figure_audit.md`](final_table_figure_audit.md) | **PARTIAL**; Table 3/4 manuscript integration과 Figure 4 asset `[MISSING]` |

Generated extraction data의 input/output hash는 [`extraction_manifest.json`](extraction_manifest.json)에 있다. 생성 스크립트는 `evaluation/build_reviewer2_revision_package.py`이며 모델이나 GPU를 호출하지 않는다.

## Comment별 완료·action 구분

| Comment | 자료 상태 | 원고 수정 | 추가 annotation | 외부 release/literature action | 핵심 제한 또는 `[MISSING]` |
|---|---|---:|---:|---:|---|
| M1 | DATA_READY | 필요 | 없음 | 없음 | Target별 paired 통계 완료 |
| M2 | DATA_READY | 필요 | 없음 | 없음 | Cohort micro-F1은 paired test에 미사용 |
| M3 | DATA_READY | 필요 | 없음 | 없음 | Cross-dimension contradiction constraint `[MISSING]`; 실제 구현상 없음이라고 공개 |
| M4 | PARTIAL | 필요 | 없음 | 없음 | Main Adaptive의 numeric candidate score/weight와 deterministic tie-break `[MISSING]`; prompted LLM policy로 기술 |
| M5 | DATA_READY | 필요 | 없음 | 없음 | Seed별 유의성이 일관되지 않음 |
| M6 | DATA_READY | 필요 | 없음 | 없음 | Direct official active-baseline reproduction `[MISSING]`; protocol adaptation이라고 명시 |
| M7 | DATA_READY | 필요 | 없음 | 없음 | 모든 dimension의 일관된 개선은 지지되지 않음 |
| M8 | DATA_READY | 필요 | 없음 | 없음 | Qwen3-8B backbone에서 개선 재현 안 됨 |
| M9 | PENDING | claim 제한 필요 | **필요** | 없음 | Annotator A/B, agreement, adjudication 모두 `[MISSING]` |
| M10 | PARTIAL | **필요** | 없음 | 없음 | Current manuscript가 없어 exact reuse inventory `[MISSING]` |
| M11 | DATA_READY | 필요 | 없음 | 없음 | 12 ablation tests 모두 BH 보정 후 비유의 |
| M12 | PARTIAL | 필요 | 없음 | 없음 | Power/depreciation/utilization/cached tokens/end-to-end wall-clock 일부 `[MISSING]` |
| m1 | DIRECTION_READY | **필요** | 없음 | 없음 | Table 3 manuscript 위치 `[MISSING]` |
| m2 | DATA_READY | **필요** | 없음 | 없음 | Final Table 4 source `[MISSING]` |
| m3 | DATA_READY | 필요 | 없음 | 없음 | 8 cases×10 methods 추출 완료; hidden chain-of-thought `[MISSING]` |
| m4 | DATA_READY | 필요 | 없음 | 없음 | 모든 Adaptive case가 5 questions; numeric early-stop threshold `[MISSING]` |
| m5 | DATA_READY | 필요 | 없음 | 없음 | 최초 question과 response realization exact-paired |
| m6 | CI_READY | **필요** | 없음 | 없음 | Figure 4 asset/script `[MISSING]` |
| m7 | MISSING_EXTERNAL | 필요 | 없음 | **Permanent release/DOI 필요** | Tag/release/DOI `[MISSING]` |
| m8 | MISSING_EXTERNAL | 필요 | 없음 | **문헌 상태 확인 필요** | `.bib`/preprint inventory/publication status `[MISSING]` |
| m9 | SOURCE_MISSING | **필요** | 없음 | 없음 | 편집 가능한 manuscript `[MISSING]` |

## 재현 명령

아래 명령은 보존된 raw results를 읽어 CSV와 감사 문서를 다시 만들 뿐 inference를 실행하지 않는다.

```bash
/opt/conda/envs/tracecal_rl/bin/python -m evaluation.build_m1_m2_reporting
/opt/conda/envs/tracecal_rl/bin/python -m evaluation.build_reviewer2_revision_package
```

## 제출 전에 반드시 남는 작업

1. 최신 manuscript `.tex`/`.bib`를 가져와 mapping의 `[MISSING]` section/table/figure label과 수정 전 문장을 채운다.
2. 140-edge graph pack을 두 사람이 독립 평가하고 adjudication/agreement를 계산하거나 graph claim을 제한한다.
3. Table 3 prior-work disclosure, Table 4 raw/baseline/gain, Figure 4 CI를 실제 원고 asset에 반영한다.
4. Submission과 대응하는 immutable code/data release와 DOI를 발행한다.
5. Preprint citation의 peer-reviewed version을 외부에서 확인한다.

위 항목은 새 model experiment가 아니다. Graph annotation은 사람 평가이고, release/reference 확인은 외부 action이며, 나머지는 원고 편집이다.
