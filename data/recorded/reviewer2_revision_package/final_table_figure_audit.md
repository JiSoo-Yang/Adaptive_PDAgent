# Final Table 3, Table 4, and Figure 4 audit

상태: **DATA_READY / MANUSCRIPT_ASSETS_PARTIALLY_MISSING**. 표와 그림에 넣을 수치는 존재하지만 편집 가능한 manuscript와 Figure 4 asset이 없어 반영 완료를 확인할 수 없다.

## Table 3

| Requirement | Current evidence | Audit result | Action |
|---|---|---|---|
| Prior-work 성격을 명확히 표시 | Reviewer decision과 이전 ICPR PDF | **NOT SATISFIED / manuscript `[MISSING]`** | Caption과 note에 reproduced/recomputed/new provenance를 표시 |
| `Original PD-Agent [4]` 명칭 | Current manuscript `[MISSING]` | **NOT VERIFIABLE** | `PD-Agent (Ours)`를 변경 |
| Supplementary 이동 | Current manuscript `[MISSING]` | **NOT VERIFIABLE** | Main-text Table 3를 supplementary로 이동하고 본문 reference 갱신 |
| Per-cell provenance | Local row files에는 없음 | **`[MISSING]`** | 각 값의 prior/new/recomputed source를 연결 |
| 최종 local source | `results/selective_gai/table_main_rows.tex`가 최신 complete row 후보; `results/tables/table3_rows.tex`는 incomplete | **NO FINAL TABLE SOURCE** | 최신 원고에서 caption/label/source를 확정 |

`results/selective_gai/table_main_rows.tex`와 `results/selective_gai/table_ablation_rows.tex`는 2026-07-31 생성 row 조각이다. Caption, label과 manuscript include 위치가 없어 그것만으로 “최신 Table 3”이라고 단정할 수 없다.

## Table 4

Reviewer m2와 M7을 충족하는 final table에는 target/model과 method별로 raw dimension metric, majority baseline, normalized gain, Average Gain을 함께 제공해야 한다.

| Requirement | Data availability | Reflected in local table row? | Source |
|---|---|---|---|
| Raw social-role accuracy | READY | 최신 row 후보에는 gain 중심이라 확인되지 않음 | `results/access_revision/main/aggregate/method_metrics.csv` |
| Raw personality accuracy | READY | 동일 | `results/access_revision/main/aggregate/method_metrics.csv` |
| Raw background accuracy | READY | 동일 | `results/access_revision/main/aggregate/method_metrics.csv` |
| Raw interests micro-F1 | READY | 동일 | `results/access_revision/main/aggregate/method_metrics.csv` |
| Majority baseline 4개 | READY | 포함 증거 없음 | `results/access_revision/m1_m2_reporting/majority_baselines.csv` |
| Normalized gain 4개 | READY | `results/selective_gai/table_main_rows.tex`에 존재하나 현재 revision method 전체를 포괄하지 않음 | method metrics CSVs |
| Average Gain | READY | 일부 row에 존재 | method metrics CSVs |
| Analysis-unit note | READY | manuscript `[MISSING]` | `results/access_revision/m1_m2_reporting/m2_metric_aggregation_and_analysis_unit.md` |
| Dimension uncertainty/test | READY | final table/caption 반영 여부 확인 불가 | `results/access_revision/m1_m2_reporting/dimension_level_tests.csv` |

Majority baselines는 held-out N=304에서 social role 118/304=0.3881578947, personality 166/304=0.5460526316, background 84/304=0.2763157895, interests 78/304=0.2565789474다. 이 값은 target model에 따라 바뀌지 않는다.

Table 4 note에는 다음을 명시해야 한다.

> Raw metrics are cohort summaries. Persona-level normalized gains are computed against the held-out majority baseline and averaged equally across the four dimensions to form Average Gain. Cohort micro-F1 is reported descriptively and is not replicated as 304 independent observations in paired tests.

Final Table 4 `.tex`/manuscript integration: **`[MISSING]`**. 기존 `results/tables/table4_rows.tex`는 일부 model만 담은 구 파일이므로 final source로 사용하지 않는다.

## Figure 4

| Requirement | Current state | Source/action |
|---|---|---|
| Figure 4 PDF/PNG/SVG | **`[MISSING]`** | Asset을 복구하거나 existing cost CSV에서 다시 그려야 함; model inference는 불필요 |
| Plot-generating script/spec | **`[MISSING]`** | 저장소에서 Figure 4 전용 source를 찾지 못함 |
| Input-token multiplier point estimate | READY | `results/access_revision/existing_runs/cost_summary.csv` |
| Output-token uncertainty | READY | `results/access_revision/existing_runs/cost_summary.csv`, `results/access_revision/audit/resource_by_cell.csv` |
| Persona-bootstrap 95% CI | READY | 위 CSV에 있음 |
| Error bar/CI가 figure에 표시됐는지 | **NOT VERIFIABLE** | Figure asset이 없음 |
| Resampling unit caption | manuscript `[MISSING]` | Caption에 persona bootstrap이라고 명시 |
| Hardware/calls/GPU-hour context | READY | `cost_audit_report.md` |

Figure 4의 error bar는 persona별 paired 또는 method별 cost record를 bootstrap한 95% CI로 표시하고, point만 표시하는 경우 동일 CI를 adjacent table에 제공해야 한다.

## Uncertainty/CI 전체 점검

| Result family | CI data | Manuscript/table/figure 반영 |
|---|---|---|
| M1 Adaptive−Original Average Gain | 10,000 paired percentile bootstrap, READY | `[MISSING]` |
| Dimension raw difference | 10,000 paired percentile bootstrap, READY | `[MISSING]` |
| Main baseline/ablation macro contrasts | 10,000 paired percentile bootstrap, READY | `[MISSING]` |
| Multi-seed/backbone contrasts | READY | `[MISSING]` |
| Input/output token cost | Persona-bootstrap CI, READY | Figure 4 `[MISSING]` |
| Budget-allocation proportions | Inferential CI/test `[MISSING]` | Descriptive count만 사용 |
| Prediction-invalid rates | Inferential CI/test `[MISSING]` | Descriptive count만 사용 |
| Graph semantic validity | Annotator result/CI/agreement `[MISSING]` | PENDING |

## 최종 수정 우선순위

1. **P0 — manuscript source 확보:** 최신 `.tex`/`.bib`와 실제 Table 3/4/Figure 4 include 위치를 연결한다.
2. **P0 — M1/M2 table:** primary target별 effect, CI, Wilcoxon, raw/BH p, counts와 exact analysis unit을 삽입한다.
3. **P0 — Table 3 disclosure:** prior-work table을 supplementary로 옮기고 `Original PD-Agent [4]` 및 per-cell provenance를 표시한다.
4. **P0 — Table 4 재구성:** raw score, majority baseline, normalized gain, Average Gain과 dimension-level uncertainty를 같이 제시한다.
5. **P0 — Figure 4:** 기존 cost CSV로 asset을 복구/재작성하고 CI와 resampling unit을 표시한다.
6. **P0 — Graph claim:** human annotation을 완료하거나 semantic-validity 주장을 제한한다.
7. **P1 — Null/negative results:** random ranking, active baseline, ablation, alternative backbone의 비유의/비재현 결과를 표와 Discussion에 포함한다.
8. **P1 — Cost limitation:** cached tokens, power, depreciation, utilization이 측정되지 않았음을 넣는다.
9. **P1 — Release/reference:** permanent DOI release와 preprint publication audit를 완료한다.

현재 상태에서 새 model experiment는 필요 없다. Figure 4 재작성은 기존 CSV를 이용한 presentation 작업이며, graph annotation과 external release/reference 확인은 별도의 사람/외부 action이다.
