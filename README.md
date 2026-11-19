# Adaptive_PDAgent 1.0.0

**Adaptive PD-Agent: Active Interviewing for LLM Persona Discovery with Bridging Inference**의 최종본에 맞춘 소프트웨어 등록용 실행 패키지입니다.

기준은 사용자가 제공한 `IEEE_Access_final_main.zip` 안의 `FINAL Article.pdf`와 `final_source.zip/main.tex`입니다. 구버전 ICPR 프로그램과 구분하여 최종 논문의 핵심인 **대화 기반 적응형 질문 선택**과, 이를 검증하는 Original·Online·Selective 비교 및 8개 추가 대조군을 실행합니다.

프로그램 폴더에는 코드, 304개 페르소나, 보존된 실험 기록, 최종 논문, 검증 결과가 들어 있습니다. 모델 다운로드부터 실험까지의 전체 절차는 **[소프트웨어등록.md](소프트웨어등록.md)**에 있습니다.

## 바로 확인

Python 3.11 이상, 아래 기본 점검은 GPU가 필요 없습니다.

```bash
cd /home/irteam/js/Adaptive_PDAgent
python -m pdaccess doctor
python -m pdaccess run \
  --manifest data/recovered/cohort_for_reimplementation.json \
  --config config/qwen1_7b.json --mock --limit 2 \
  --output results/my_smoke
```

`--mock`는 배관·규칙 검사용 합성 응답입니다. 실제 LLM 성능이나 논문 재현 결과로 해석하지 않습니다. 실제 실행은 모델 서버를 준비한 뒤 `--mock`를 제거합니다.

## 두 실행 경로

| 목적 | 명령 | 결과 의미 |
|---|---|---|
| 최종 논문의 주 비교 통계 재검산 | `python -m pdaccess audit-paper --output results/my_paper_audit` | 보존된 실제 점수 재분석 및 최종 TeX 표 대조. 새 추론 아님 |
| 로컬 모델로 새 인터뷰 | `python -m pdaccess run ...` | 명시된 재구현으로 수행한 새 실험 |
| 새 실험 통계·비용 집계 | `python -m pdaccess summarize <실험폴더> --output <보고서폴더>` | paired AG·Wilcoxon/BH·bootstrap·McNemar·토큰/턴 비교 |
| 원 로그에서 근거 다시 추출 | `python -m pdaccess recover data/recorded <새폴더>` | 보존된 요청·응답·페르소나·pairing 검증 |

통계 분석에는 `requirements-analysis.txt`가 필요합니다. `results/final_paper_audit/`에는 실제 실행한 재검산 결과가, `results/synthetic_smoke/`에는 합성 점검 결과가 포함됩니다.

## 포함된 방법

| 구분 | 실행 이름 | 내용 |
|---|---|---|
| 기준 | `original` | 고정 최대 5턴의 일반 질문 정책 |
| **논문의 핵심 기여** | **`adaptive`** | 대화만으로 부족한 차원을 판단하고 세 질문 후보 생성·평가·선택 |
| 그래프 비교 | `online`, `selective` | 매 턴 그래프 사용 / actionability gate·utility에 따른 선택적 사용 |
| 강한 대조군 | `random_candidate`, `round_robin`, `dialogue`, `generic` | 후보 무작위 선택·차원 순환·대화 후속·일반 컨트롤러 |
| 구성요소 제거 | `direct`, `no_coverage`, `no_redundancy` | 후보 목록·coverage·redundancy 지시 제거 |
| 불확실성 대조군 | `uncertainty` | 다섯 확률적 예측의 정규화 entropy로 차원 선택 |

Adaptive의 질문 선택에는 그래프나 호스트의 고정 가중합을 넣지 않습니다. 모든 방법의 최종 예측에는 공통 대화·bridging graph 표현을 사용합니다. 그래프 utility는 Selective에만 적용됩니다.

## 폴더 구성

```text
Adaptive_PDAgent/
  pdaccess/               인터뷰·그래프·규칙·모델 호출·통계 분석
  config/                 스키마·복구 프롬프트·모델별 설정·고정 revision
  data/recovered/         304개 페르소나와 복구된 프롬프트·근거
  data/recorded/          제공된 실제 실험 기록 및 통계 입력
  paper/                  최종 PDF·TeX·원본 소스 ZIP
  tools/                  모델 다운로드·로컬 서버 시작·연결 검사
  tests/                  규칙·pairing·HTTP 호출·통계 검증
  docs/                   최종 논문 대응표·출처·검증 범위
  results/                재검산·합성 점검 및 새 실험 결과
  소프트웨어등록.md       프로그램 설명과 설치·다운로드·실행 전체 절차
```

## 구현의 범위

`persona/access_reimplementation`은 역사적 원 실험 소스가 아닌 재구현 코드입니다. 이를 기반으로 실행 패키지를 구성했습니다. 주요 질문·예측 프롬프트는 실제 로그에서 복구했으나 Online/Selective 일부 프롬프트, 문자열 정규화·매칭, 시드 파생과 직렬화 등에는 재구현이 포함됩니다. 특히 Selective의 integrated extraction/state 프롬프트는 본 패키지에서 명시적으로 보완한 구현입니다.

실제 모델 가중치 다운로드와 GPU 추론은 이 패키지 제작 중 수행하지 않았습니다. CPU 통계 재검산·규칙·합성 흐름 테스트와 실제 모델 실행 검증을 구분합니다. 자세한 대응 및 차이는 [docs/PAPER_MAPPING.md](docs/PAPER_MAPPING.md), 검증 결과는 [docs/VALIDATION.md](docs/VALIDATION.md)에 있습니다.

## GitHub에서 받기

저장소: https://github.com/JiSoo-Yang/Adaptive_PDAgent

대용량 원 실험 JSONL 기록은 Git LFS로 관리한다. Git LFS를 설치한 후 다음 명령으로 코드와 데이터를 함께 받는다. GitHub의 Download ZIP만으로는 LFS 데이터가 포함되지 않을 수 있다.

```bash
git lfs install
git clone https://github.com/JiSoo-Yang/Adaptive_PDAgent.git
cd Adaptive_PDAgent
git lfs pull
```
