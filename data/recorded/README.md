# Access revision results — start here

논문 수정용 시작점은 [`reviewer2_revision_package/README.md`](reviewer2_revision_package/README.md)다. Reviewer 2의 M1–M12와 m1–m9를 13개 산출물, 현재 상태, 원고 반영 위치, `[MISSING]` 항목으로 연결한다.

## 폴더 구성

| 경로 | 용도 | 논문 수정 시 필요성 |
|---|---|---|
| `reviewer2_revision_package/` | 전체 revision mapping, baseline/ablation/cost/schema/qualitative/prior-work audit | **가장 먼저 확인** |
| `m1_m2_reporting/` | M1/M2 full report, 9,728행 raw CSV, LaTeX table row, dimension tests | **필수** |
| `main/aggregate/` | Strong baseline와 ablation 최종 집계 | **필수** |
| `active_information_gain/main/aggregate/` | Adapted active-uncertainty baseline 최종 집계 | **필수** |
| `robustness/aggregate/` | Multi-seed와 alternative-backbone 결과 | **필수** |
| `audit/` | 설정, token, validity, GPU-hour 감사 | **필수** |
| `graph_validity/` | 140-edge annotation pack과 manifest | **필수; 사람 annotation 대기** |
| `existing_runs/` | 기존 held-out primary 결과와 audit | M1 source 확인에 필요 |
| `main/raw/` | 10,944 final main run 원로그 | 재현성과 all-method qualitative trace의 source라 유지 |
| `active_information_gain/main/raw/` | 1,216 active baseline 원로그 | 재현성 근거라 유지 |
| `robustness/seed3/raw/`, `robustness/backbone_qwen3_8b/raw/` | Robustness 원로그 | 재현성 근거라 유지 |
| 각 `logs/` | Runtime, 성공 여부, 비용 감사 | 크기가 작고 M12 근거라 유지 |
| `experiment_summary.md` | 전체 실험 요약 | 빠른 overview |

## 정리한 항목

최종 보고서가 참조하지 않는 다음 debug-only 산출물은 2026-09-15에 삭제했다.

- 초기 `smoke/`
- active baseline `smoke/`
- active baseline `paired_smoke/`
- 첫 질문/응답 pairing이 맞지 않아 폐기한 `unpaired_batch_diagnostic_20260913/`

최종 결과와 연결된 raw/log 파일은 논문 수치, 정성 사례와 재현성의 근거이므로 유지했다.

## 빠른 작업 순서

1. `reviewer2_revision_package/manuscript_source_and_mapping.md`
2. `m1_m2_reporting/m1_primary_summary_table.tex`
3. `reviewer2_revision_package/final_table_figure_audit.md`
4. `reviewer2_revision_package/prior_work_and_release_audit.md`
5. `reviewer2_revision_package/graph_validity_annotation_report.md`

Raw inference를 직접 확인할 필요가 없으면 `main/raw/`, `active_information_gain/main/raw/`, `robustness/*/raw/`는 열지 않아도 된다.
