# M1/M2 reporting package

이 폴더는 Reviewer 2의 M1/M2 지적과 연관된 pairing·dimension 분석을 원고와 response letter에 정확히 옮기기 위한 자료다. 모델 추론을 새로 수행하지 않았으며, 동결된 304-persona held-out 결과를 재집계했다.

## 핵심 보고서

- `m1_primary_statistical_analysis_full_report.md`: target별 주 비교 통계, 최종 표, 해석과 limitation
- `m2_metric_aggregation_and_analysis_unit.md`: persona/cohort 지표 구분, 수식, Wilcoxon 관측값, micro-F1 처리
- `dimension_level_statistical_test_report.md`: 16개 exact McNemar 검정과 차원별 해석
- `pairing_and_sampling_audit.md`: 동일 persona·최초 문답 pairing, sampling, seed, split, 평가 수
- `manuscript_and_response_mapping.md`: 원고 및 reviewer response 반영 위치와 삽입용 문장
- `data_schema.md`: CSV 필드, 키, 재현 방법

## 재현 자료

- `M1_M2_raw_results.csv`: 요청 field를 그대로 갖춘 9,728행 long-format 자료(4 targets × 304 personas × 2 methods × 4 dimensions)
- : 요청 field를 그대로 갖춘 9,728행 long-format 자료(4 targets × 304 personas × 2 methods × 4 dimensions)
- `m1_persona_level.csv`: 4 targets × 304 personas = 1,216 paired 관측값
- `m1_primary_summary.csv`: 4개 target의 Wilcoxon·bootstrap·BH 전체 값
- `m1_primary_summary_table.tex`: 주 결과 표의 LaTeX 초안
- `dimension_level_tests.csv`: 4 targets × 4 dimensions = 16개 McNemar 결과
- `pairing_sampling_audit.csv`: 4 targets × 4 source methods = 16개 완전성 감사 행
- `majority_baselines.csv`: dimension별 majority rule과 baseline
- `manifest.json`: 입력·출력 SHA-256, software version, sampling audit

## 명칭

- `original` = Original PD-Agent
- `dialogue_only` = Adaptive PD-Agent
- 모든 차이는 `Adaptive - Original` 방향이다.

재현 명령:

```bash
/opt/conda/envs/tracecal_rl/bin/python -m evaluation.build_m1_m2_reporting
```

이 명령은 저장된 JSONL을 읽어 통계와 CSV만 다시 만든다. 모델이나 GPU를 호출하지 않는다.

