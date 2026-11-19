# Manuscript and reviewer-response mapping for M1/M2

현재 workspace에는 결정문 PDF와 분석 자료는 있지만 수정 가능한 IEEE Access 원고 `.tex`/`.docx` 및 response letter 원본이 없다. 따라서 아래의 section 역할은 확정할 수 있으나, 실제 section/table 번호와 page/line은 `[MISSING]`로 표시한다.

## 반영 위치

| 결과/설명 | 원고 반영 위치 | Table/Figure | Reviewer response | 근거 파일 | 상태 |
|---|---|---|---|---|---|
| 304-persona held-out split, cohort/run seed, unique sampling, 제외 0 | Experiments 또는 Experimental Setup의 Data/Sampling subsection; 번호 `[MISSING]` | Supplementary sampling table 번호 `[MISSING]` | R2-M3, R2-m5; R1-2 확인 근거 | `pairing_and_sampling_audit.md`, `pairing_sampling_audit.csv` | 자료 완료, 원고 삽입 대기 |
| 네 method에서 동일 persona·ground truth·최초 질문·최초 응답 | Experimental Setup의 Paired Protocol paragraph; 번호 `[MISSING]` | 본문 표 불필요; detailed audit는 supplement | R2-M3, R2-m5 | `pairing_sampling_audit.csv` | 자료 완료, 원고 삽입 대기 |
| Dimension score와 cohort metric 구분 | Methods의 Evaluation Metrics subsection; 번호 `[MISSING]` | 기존 metric table 또는 신규 definition table 번호 `[MISSING]` | R2-M2 | `m2_metric_aggregation_and_analysis_unit.md` | 문구·수식 완료 |
| Majority baseline과 normalized gain 공식 | Methods의 Evaluation Metrics subsection, Average Gain 정의 직전/직후 | 기존 equation 번호의 교체/추가 번호 `[MISSING]` | R2-M2, R2-M3, R2-m2 | `m2_metric_aggregation_and_analysis_unit.md`, `majority_baselines.csv` | 수식 완료 |
| Persona-level Average Gain 공식과 Wilcoxon 관측값 | Methods의 Statistical Analysis subsection; 없으면 신규 subsection | Equation 번호 `[MISSING]`; figure 불필요 | R2-M1, R2-M2 | `m2_metric_aggregation_and_analysis_unit.md` | 수식 완료 |
| Wilcoxon 옵션, 10,000회 paired percentile bootstrap, target별 seed, 4-test BH family | Methods의 Statistical Analysis subsection | 본문 주 결과 표의 note | R2-M1 | `m1_primary_statistical_analysis_full_report.md` | 세부값 완료 |
| Target별 Original/Adaptive 평균, Δ, CI, W, raw/BH p, +/−/tie | Results의 Adaptive vs Original primary comparison subsection; 번호 `[MISSING]` | **신규 main results table**, 정확한 번호 `[MISSING]`; `m1_primary_summary_table.tex` 사용 | R2-M1 | `m1_primary_summary.csv` | 표 완료 |
| 16개 dimension McNemar와 BH family | Methods의 Statistical Analysis에 test 정의; Results의 Dimension-level Analysis에 결과 | 상세 16행은 Supplementary Table 번호 `[MISSING]` | R2-M2, R2-M7 | `dimension_level_statistical_test_report.md`, `dimension_level_tests.csv` | 표 완료 |
| Raw dimension score, majority baseline, normalized gain | Results의 현재 Table 4 설명과 표 | Reviewer가 지목한 **Table 4**에 세 값 모두 추가; 실제 cell layout `[MISSING]` | R2-m2, R2-M7 | `majority_baselines.csv`, 기존 `main/aggregate/method_metrics.csv` | M1/M2 정의 완료; Table 4 편집 대기 |
| Background에 집중된 개선, interests의 target별 방향 차이 | Results의 Dimension-level Analysis와 Discussion | Figure는 필수 아님; optional forest plot 번호 `[MISSING]` | R2-M7 | `dimension_level_statistical_test_report.md` | 해석 완료 |
| Qwen3-1.7B null, Gemma의 Wilcoxon/mean-CI 불일치, target·dimension 이질성 | Discussion/Limitations 및 Conclusion의 claim 축소 | 표 footnote 또는 Limitations; 신규 figure 불필요 | R2-M1, R2-M7 | M1 및 dimension report | 문구 완료 |
| Persona별 재현 데이터와 source/output hash | Data/Code Availability, Supplementary Material | Supplementary CSV/repository artifact | R2-M1, R2-M2, R2-m7 | `m1_persona_level.csv`, `manifest.json`, `data_schema.md` | 로컬 자료 완료; 영구 release/DOI는 `[MISSING]` |

Figure 4는 token-cost uncertainty 요구에 대응하는 그림이므로 M1/M2 통계 정의를 억지로 넣지 않는다. M1/M2에는 표와 Methods 수식이 직접적인 전달 방식이다.

## 원고 Methods 삽입용 영문

### Metric and analysis unit

> For persona (i), method (m), and dimension (d), we defined the majority-normalized gain as (G_{i,d}^{(m)}=(s_{i,d}^{(m)}-B_d)/(1-B_d)), where (s_{i,d}^{(m)}) is the persona-level dimension score and (B_d) is the majority baseline computed once from the 304-persona frozen held-out cohort. The persona-level Average Gain was (AG_i^{(m)}=\frac{1}{4}\sum_d G_{i,d}^{(m)}). The four dimensions received equal weight.

> The persona-level scores were coarse-category correctness for social role, exact yes/no correctness for the sampled Big-Five trait, exact value correctness for the sampled background category, and set F1 for interests. The current interests schema contains one gold and one predicted value per persona; consequently, the observed persona-level interest F1 values were binary. Corpus-level micro-F1 was reported descriptively and was not duplicated or treated as 304 independent observations.

### Statistical analysis

> For each target model, the primary paired observation was \(\Delta_i=AG_i^{(Adaptive)}-AG_i^{(Original)}\) for each of the 304 held-out personas. We applied a two-sided paired Wilcoxon signed-rank test using SciPy 1.17.1 (`zero_method='wilcox'`, no continuity correction, and `method='auto'`, which resolved to the asymptotic method at this sample size). We estimated a 95% confidence interval for the mean paired difference with 10,000 ordinary percentile bootstrap replicates, resampling persona pairs with replacement. We controlled the four target-level primary tests as one Benjamini–Hochberg family. For each binary dimension, we used an exact two-sided McNemar test and controlled the 16 target-by-dimension tests as a separate Benjamini–Hochberg family.

### Pairing and sampling

> All methods used the same 304 unique frozen held-out personas (cohort seed 20260802). For every target-persona bundle, the persona ID, ground truth, first question string, and first response string were exactly identical across methods. Every target-method cell contained 304 successful evaluations, with no missing, duplicate, or excluded persona indices. The held-out runs used base seed 20260831.

## 원고 Results 삽입용 영문

> Adaptive PD-Agent produced positive mean persona-level Average Gain differences for all four target models: +0.0190 for Qwen3-1.7B, +0.0397 for Qwen3-4B, +0.0536 for Llama-3.2-3B-Instruct, and +0.0281 for Gemma-3-4B-IT. The paired-bootstrap 95% confidence intervals excluded zero for Qwen3-4B [+0.0046, +0.0753] and Llama-3.2-3B-Instruct [+0.0181, +0.0901], but included zero for Qwen3-1.7B [−0.0139, +0.0519] and Gemma-3-4B-IT [−0.0088, +0.0656]. After Benjamini–Hochberg correction across the four Wilcoxon tests, the adjusted p-values were 0.2112, 0.0301, 0.0048, and 0.0301, respectively.

> Dimension-level improvements were not uniform. After correction across the 16 exact McNemar tests, positive differences remained significant for background with Llama-3.2-3B-Instruct (b=18, c=48, adjusted p=0.0046) and Gemma-3-4B-IT (b=16, c=41, adjusted p=0.0101). No other target-dimension contrast survived this correction.

## Limitation 삽입용 영문

> These results do not establish a uniform benefit across target models or persona dimensions. Qwen3-1.7B was not significant in the primary family, and the Gemma signed-rank result passed the 0.05 BH threshold while the bootstrap confidence interval for the mean difference included zero. Improvements that survived dimension-level correction were concentrated in background inference for two targets. Moreover, Average Gain is relative to the majority distribution of this frozen synthetic persona cohort and may change under a different persona distribution.

## Reviewer response 삽입용 영문

### R2-M1

> We thank the reviewer for requesting a fully paired primary analysis. We now report all 304 persona-level pairs for each target, including Original and Adaptive mean Average Gain, the paired mean difference, the Wilcoxon statistic and raw p-value, the effective nonzero sample size, positive/negative/tied pair counts, 10,000-replicate paired percentile-bootstrap confidence intervals and seeds, and Benjamini–Hochberg adjusted p-values. The four target-level Average Gain tests constitute one correction family. The complete values appear in Table `[MISSING]`, and the persona-level inputs are provided in Supplementary Data `[MISSING]`.

### R2-M2

> We clarified the distinction between persona-level observations and cohort-level metrics. The Wilcoxon test receives 304 persona-level differences in equally weighted, majority-normalized Average Gain for each target. Cohort-level micro-F1 is reported as a descriptive cell summary; it is not replicated into persona-level observations. Because the current interest labels are singleton sets, the observed per-persona interest F1 is binary. We therefore used paired persona-level correctness outcomes for exact McNemar tests on each dimension and corrected the 16 target-by-dimension tests as a separate family. These definitions and equations now appear in Section `[MISSING]`.

### R2-M3 and R2-m5 pairing point

> We audited the raw run bundles and confirmed that all four methods used the same 304 unique held-out personas for every target. Persona IDs, ground truths, first-question strings, and first-response strings matched exactly across methods. Each target-method cell contains 304 successful evaluations, with no missing, duplicate, replacement-reused, or excluded persona indices. We added these details to Section `[MISSING]` and Supplementary Table `[MISSING]`.

## 편집 시 확인할 항목

- 수정 원고의 실제 section/equation/table/page/line 번호: `[MISSING]`
- 신규 primary statistical table 번호: `[MISSING]`
- 16행 dimension table의 supplementary 번호: `[MISSING]`
- 기존 Table 4에서 raw score/baseline/gain을 배치할 정확한 열 구조: `[MISSING]`
- response letter의 highlighted manuscript page/line 참조: `[MISSING]`
- 저장소 영구 release URL 또는 DOI: `[MISSING]`
- `α=0.05`가 사전 protocol/기존 원고에 명시됐는지: `[MISSING]`

