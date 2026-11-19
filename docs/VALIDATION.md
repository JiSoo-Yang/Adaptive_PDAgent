# 검증 기록

검증일: 2026-11-19. CPU 환경에서 수행했다.

| 검증 | 결과 및 근거 |
|---|---|
| 단위·통합 검사 | 14개 통과. `results/validation/tests.log` |
| 합성 인터뷰 | 2 persona × 12 방법 = 24개 완료. `results/synthetic_smoke/` |
| 합성 결과 분석 | 통계·비용 CSV 생성 완료. `results/synthetic_report/`. 모델 성능 증거가 아님 |
| 원 로그 복구 | 21개 원 파일에서 304개 persona 복구. `results/recovery_check/recovery_manifest.json` |
| 보존된 기록 | main 10,944 + uncertainty 1,216 + robustness 1,000 = 13,160개 인터뷰 |
| 주 비교 통계 | 원 dimension-score 9,728행 재계산. 네 target의 최종 논문 표 대조 40개 항목 모두 통과 |
| 최종본 일치 근거 | `results/final_paper_audit/final_paper_audit.json`: `all_checks_passed=true`, `reference_inputs_match=true` |
| 문법·도구 | Python compileall, run.sh Bash 문법, 모델 다운로드·서빙 명령 dry-run 통과 |

최종 표 대조는 표의 인쇄 정밀도에 따른 반올림 오차를 허용한다. 기존 점수 재분석이며 새 모델 추론 결과가 아니다. 실제 가중치 다운로드, vLLM 서버 시작, GPU 메모리 측정 및 실제 모델 인터뷰는 수행하지 않았다.

주요 프롬프트와 persona는 로그에서 복구했지만 역사적 원 실험 소스 전체는 확보되지 않았다. 이 패키지는 명시된 재구현을 실행한다. 정확한 제한은 `PAPER_MAPPING.md`를 참조한다. `REIMPLEMENTATION_ORIGIN.md`는 기반 프로젝트의 원본 설명을 보존한 기록이므로 그 안의 과거 상대 경로는 현재 실행 안내가 아니다.

현재 설치·실행 절차는 루트의 `소프트웨어등록.md`를 따른다. 분석 환경 NumPy 2.2.6 / SciPy 1.17.1로 통계 검증을 수행했다.

`bundle_sha256.json`은 배포 코드·설정·문서·데이터·논문의 상대 경로별 SHA-256 목록이다. 가상환경, 모델 가중치, 실행 결과와 캐시는 목록에서 제외했다. 원본 출처 정보는 별도 `provenance.json`에 있다.
