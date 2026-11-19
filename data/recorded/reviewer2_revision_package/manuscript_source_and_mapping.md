# Manuscript source and Reviewer 2 mapping

상태: **PARTIAL / MANUSCRIPT_SOURCE_MISSING**. 이 문서는 Reviewer 2의 M1–M12와 m1–m9를 수정 원고에 옮길 위치를 지정한다. 저장소에 편집 가능한 최신 Access 원고가 없으므로 실제 section 번호, table/figure 번호, 현재 문장과 line number는 추측하지 않고 `[MISSING]`으로 둔다.

## 원고 source inventory

| Asset | 확인된 최신 local 경로 | 상태와 사용 범위 |
|---|---|---|
| IEEE Access 수정 원고 `.tex`/`.docx` | `[MISSING]` | 저장소 전체에서 찾지 못함. 외부 경로로 언급된 `/Users/jisu/Downloads/ACCESS_latex_template_20260513/access.tex`도 이 작업공간에는 없음 |
| Bibliography `.bib` | `[MISSING]` | 저장소 전체에서 찾지 못함 |
| 현재 제출 PDF | `[MISSING]` | 결정문만 있고 심사 대상 manuscript PDF는 없음 |
| Reviewer decision | `IEEE Access - Decision on Manuscript ID Access-2026-38546.pdf` | Reviewer comment의 source of truth |
| 이전 ICPR 논문 | `docs/papers/ICPR_2026_persona_camera_ready__유료_.pdf` | M10 prior-work 관계 감사에 사용 |
| 최신 complete main-table row 후보 | `results/selective_gai/table_main_rows.tex` | 2026-07-31 생성. Caption·label·본문 table number가 없어 실제 Table 3/4 연결은 `[MISSING]` |
| 최신 ablation-table row 후보 | `results/selective_gai/table_ablation_rows.tex` | 2026-07-31 생성. Selective-GAI ablation용 |
| 구 Table 3 row | `results/tables/table3_rows.tex` | 파일 자체가 incomplete라고 표시되어 최종 원고 source로 쓰면 안 됨 |
| 구 Table 4 row | `results/tables/table4_rows.tex` | 일부 model만 담은 구 산출물; final table 아님 |
| Figure 1 | `figures/figure1.pdf`, `figures/figure1.png` | 존재 |
| Figure 2 | `figures/figure2.pdf`, `figures/figure2.png` | 존재 |
| Figure 3 | `figures/figure3.pdf`, `figures/figure3.png` | 존재 |
| Figure 4 source/image | `[MISSING]` | 저장소 전체에서 찾지 못함; CI source data만 존재 |

따라서 아래의 “정확한 위치”는 section/table/figure의 **논리적 위치**까지 확정한 것이다. 실제 `\section` label, table number, figure filename과 수정 전 원문은 편집 가능한 원고를 가져온 뒤 연결해야 한다.

## Major comments M1–M12

| ID | 반영 위치 | 수정 전 문장 | 수정 후 문장 또는 방향 | 근거 자료 | 필요한 action |
|---|---|---|---|---|---|
| M1 | Methods의 Statistical Analysis; Results의 primary Adaptive-vs-Original subsection; primary-results table | `[MISSING]` | Target별 N=304, Original/Adaptive mean Average Gain, paired difference, Wilcoxon statistic/raw p, +/−/tie, 10,000회 paired percentile-bootstrap CI, 4-test BH q를 함께 보고한다. CI와 검정이 엇갈리는 Gemma도 그대로 쓴다. | `../m1_m2_reporting/m1_primary_statistical_analysis_full_report.md`, `../m1_m2_reporting/m1_primary_summary_table.tex` | **MANUSCRIPT_EDIT_ONLY** |
| M2 | Methods의 Metrics and Analysis Unit; M1 table note | `[MISSING]` | Persona-level 네 dimension score와 cohort-level micro-F1을 분리한다. Wilcoxon 관측값은 각 persona의 네 majority-normalized gain 평균이라고 정의하며 cohort micro-F1은 paired test에 넣지 않았다고 명시한다. | `../m1_m2_reporting/m2_metric_aggregation_and_analysis_unit.md` | **MANUSCRIPT_EDIT_ONLY** |
| M3 | Methods의 Persona Schema/Sampling; Supplementary schema/frequency table; Experimental Setup의 pairing paragraph | `[MISSING]` | Hierarchical-uniform category/value sampling, 43 social occupations, 10 Big-Five polarity values, 25 background values, 59 interest values, 634,250 raw combinations, seeds/split/frequency를 보고한다. Cross-dimension plausibility constraint가 없었다고 명시한다. | `schema_sampling_pairing_audit.md`, `sampling_probabilities_and_frequencies.csv` | **MANUSCRIPT_EDIT_ONLY** |
| M4 | Methods의 Adaptive Question Policy; Supplementary prompt/protocol appendix | `[MISSING]` | 실제 controller는 세 candidate와 짧은 rationale을 생성하고 LLM이 선택하는 prompted policy라고 기술한다. Candidate score range/weights, deterministic utility computation과 tie-break가 구현됐다는 표현은 근거가 없어 `[MISSING]`으로 두거나 삭제한다. Parsing/fallback과 JSON schema를 공개한다. | `implementation_protocol_report.md`; `evaluation/table3_table4.py`; `evaluation/run_table3_table4_vllm.py` | **MANUSCRIPT_EDIT_ONLY** |
| M5 | Experimental Setup의 Reproducibility; Supplementary model/config table; Robustness subsection | `[MISSING]` | Exact checkpoint/config/seed/hardware와 3 generation-seed 결과를 보고하고, seed별 유의성이 일관되지 않았다고 쓴다. | `../robustness/aggregate/report.md`, `../robustness/aggregate/seed_effects.csv`, `../audit/resource_and_reproducibility.json` | **MANUSCRIPT_EDIT_ONLY** |
| M6 | Experimental Setup의 Baselines; Results의 strong-baseline table; Supplementary protocol | `[MISSING]` | Random candidate, round-robin, dialogue follow-up, controller-matched generic과 adapted active uncertainty sampling의 protocol 및 null results를 보고한다. Active baseline은 official implementation reproduction이 아니라 protocol adaptation이라고 표시한다. | `baseline_comparison_report.md`; `../../../docs/access_active_information_gain_baseline.md` | **MANUSCRIPT_EDIT_ONLY**; direct official reproduction은 `[MISSING]`이나 현재 적응 baseline을 정직하게 보고하면 새 실행은 필수 아님 |
| M7 | Results의 Dimension-level Analysis; Table 4; Discussion/Conclusion | `[MISSING]` | 차원별 raw metric, baseline, gain과 exact McNemar b/c, raw/BH p를 제시한다. 일부 background 효과만 보정 후 유의했고 방향이 target마다 달랐다고 써서 all-dimension improvement 주장을 제한한다. | `../m1_m2_reporting/dimension_level_statistical_test_report.md`, `tradeoff_prediction_ablation_report.md` | **MANUSCRIPT_EDIT_ONLY** |
| M8 | Results의 Robustness; Supplementary backbone table; Limitations | `[MISSING]` | Qwen3-14B와 Qwen3-8B interviewer 비교를 추가하고, 대체 backbone에서 효과가 재현되지 않았다는 Δ, CI, p를 본문에 포함한다. | `../robustness/aggregate/backbone_robustness.csv`, `../robustness/aggregate/report.md` | **MANUSCRIPT_EDIT_ONLY** |
| M9 | Methods의 Graph Construction/Validation; Results 또는 Supplementary graph-validity subsection; Limitations | `[MISSING]` | 완료 전에는 graph를 “LLM-generated, exact-span-grounded intermediate representation”으로만 부르고 semantic validity가 확인됐다는 표현을 삭제한다. 최종본에 강한 graph claim을 유지하려면 두 annotator와 adjudication 결과를 채운다. | `graph_validity_annotation_report.md`, `../graph_validity/annotation_sample.csv` | **ADDITIONAL_ANNOTATION_REQUIRED / PENDING** |
| M10 | Related Work; prior-work comparison paragraph; Table 3 caption/row label; Previously Published Statement | `[MISSING]` | Table 3를 prior-work reproduction/adaptation으로 명확히 표시하고 `PD-Agent (Ours)`를 `Original PD-Agent [4]`로 바꾼다. Reused/adapted entries, text, methods, illustrations를 열거하고 “re-examined using the per-dimension protocol”이 무엇을 재계산했는지 명시한다. | `prior_work_and_release_audit.md`, 이전 ICPR PDF | **MANUSCRIPT_EDIT_ONLY**; exact reuse diff는 current manuscript가 없어 `[MISSING]` |
| M11 | Introduction의 Contributions; Methods의 policy description; Results의 Ablation; Discussion | `[MISSING]` | 학습되거나 formal optimization된 acquisition model이 아니라 LLM-prompted controller임을 명시한다. Direct generation/no coverage/no redundancy/random ranking 결과를 모두 보고하고 12개 보정 검정이 유의하지 않았다고 쓴다. | `tradeoff_prediction_ablation_report.md`, `../main/aggregate/paired_tests.csv` | **MANUSCRIPT_EDIT_ONLY** |
| M12 | Results의 Efficiency/Cost; Figure 4 또는 supplementary resource table; Limitations | `[MISSING]` | Calls, input/output tokens, H200 GPU-hours, local API fee를 보고한다. Cached-token split, power, depreciation, facility overhead, utilization trace, complete end-to-end wall-clock은 `[MISSING]`/not measured라고 명시한다. | `cost_audit_report.md`, `../audit/resource_by_cell.csv` | **MANUSCRIPT_EDIT_ONLY**; 누락 계측값을 새로 만들지 말고 limitation 처리 |

## Minor comments m1–m9

| ID | 반영 위치 | 수정 전 문장/상태 | 수정 후 문장 또는 방향 | 근거 자료 | 필요한 action |
|---|---|---|---|---|---|
| m1 | 기존 Table 3와 그 본문 참조 | `[MISSING]` | Prior-work 중심 Table 3를 supplementary로 옮기고 본문에는 핵심 차이만 요약한다. | `prior_work_and_release_audit.md` | **MANUSCRIPT_EDIT_ONLY** |
| m2 | Table 4 caption/body/note | 현재 local row 후보는 normalized gain 중심이며 raw metric과 majority baseline을 함께 제시하지 않음 | 각 target×method×dimension에 raw score, majority baseline, normalized gain을 함께 제시하고 Average Gain 식을 note에 쓴다. | `../main/aggregate/method_metrics.csv`, `../m1_m2_reporting/majority_baselines.csv` | **MANUSCRIPT_EDIT_ONLY** |
| m3 | Results의 Qualitative Cases; Supplementary case appendix | 기존 `qualitative_pairs.jsonl`은 두 method만 포함 | 8 target-case 각각에 Original, Adaptive, 네 strong baselines, 세 ablations, active uncertainty의 질문·응답·observable trace·graph·prediction을 연결한다. Extreme-case selection임을 밝힌다. | `qualitative_cases_all_methods.md`, `qualitative_cases_all_methods.jsonl` | **MANUSCRIPT_EDIT_ONLY** |
| m4 | Methods의 stopping rule; Results/Limitations | `[MISSING]` | Maximum 5 questions였고 held-out 모든 Adaptive case가 5개 질문을 사용해 early stop이 한 번도 작동하지 않았다고 두드러지게 쓴다. Numerical stopping threshold는 `[MISSING]`이다. | `implementation_protocol_report.md`, pairing audits | **MANUSCRIPT_EDIT_ONLY** |
| m5 | Experimental Setup의 Paired Protocol | `[MISSING]` | Methods가 같은 prompt template만 공유한 것이 아니라 persona별 최초 question 문자열과 최초 response realization도 exact-identical이었다고 명시한다. | `schema_sampling_pairing_audit.md`, `revision_methods_pairing_audit.csv` | **MANUSCRIPT_EDIT_ONLY** |
| m6 | Figure 4 caption/error bars; resource table | Figure 4 asset `[MISSING]` | Persona-bootstrap 95% CI를 error bar 또는 table CI로 표시하고 resampling unit을 persona라고 쓴다. | `../existing_runs/cost_summary.csv`, `../audit/resource_by_cell.csv` | **MANUSCRIPT_EDIT_ONLY**; Figure 4 source/image 복구 또는 재작성 필요, 새 inference 불필요 |
| m7 | Data/Code Availability; response letter | Permanent release와 DOI `[MISSING]` | 제출 결과에 해당하는 immutable tag/release와 DOI를 만든 후 exact identifier를 기재한다. | `prior_work_and_release_audit.md` | **EXTERNAL_RELEASE_ACTION_REQUIRED** |
| m8 | References/Related Work | `.bib`와 preprint inventory `[MISSING]` | 모든 preprint의 peer-reviewed publication 여부를 확인하고 해당 경우 bibliography를 갱신한다. | `prior_work_and_release_audit.md` | **EXTERNAL_LITERATURE_CHECK + MANUSCRIPT_EDIT_REQUIRED** |
| m9 | 원고 전체; 특히 Introduction/Methods/Results | 편집 가능한 원고가 없어 `[MISSING]` | 30–35단어 이상 문장을 나누고 `Target LLM`, `persona-discovering method`, method names와 대소문자를 일관되게 교정한다. | current manuscript `[MISSING]` | **MANUSCRIPT_EDIT_REQUIRED** |

## 삽입 우선순위

1. 편집 가능한 최신 원고와 `.bib`를 이 저장소에 가져와 실제 section/table/figure label과 현재 문장을 연결한다.
2. M1/M2/M3/M5–M8/M11/M12 및 m2–m6의 준비된 수치와 제한 문장을 반영한다.
3. M10/m1의 prior-work 선언과 Table 3 명칭·위치를 정정한다.
4. M9 annotation을 완료하거나 graph claim을 제한한다.
5. m7 permanent release/DOI와 m8 문헌 확인을 수행한 뒤 식별자와 갱신된 citation을 넣는다.
6. m9 language pass를 마지막에 수행한다.
