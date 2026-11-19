# 최종 논문과 소프트웨어 대응

기준: 제공된 최종 ZIP의 `paper/main.tex` 및 `paper/FINAL_Article.pdf`. 기존 `persona/final_revision/access_revision.tex`와 비교했을 때 변경은 사사, 초록·키워드 줄바꿈, Figure 4 파일명에 해당하며 방법·수식·주 비교 수치는 동일합니다. 최종 ZIP 해시는 `provenance.json`에 기록했습니다.

| 최종 논문 항목 | 구현 | 검증/주의점 |
|---|---|---|
| Adaptive Interviewing 및 Algorithm 1 | `runner.py`, `prompts.py`의 adaptive 경로 | 대화만으로 후보 생성·평가·선택. selected_question 직접 사용. 후보 개수·점수 범위를 새로 강제하지 않음 |
| Bridging Extraction | `core.Graph.update` | 현재 응답의 casefold·공백 정규화 연속 span 검증, 이름 정규화·edge 중복 제거 |
| Graph Evidence State | `core.Graph.state` | missing/partial/covered, `min(1,.25n+.15e+.10min(s,2))`, 최근 두 novelty |
| Actionability Gate | `core.gate` | grounded competition 또는 partial confidence≥.35 또는 두 턴 stagnation≤.10 |
| Selective utility | `core.utility`, `runner.py` | 0.30C+0.25D+0.25N−0.15R−0.05L, [0,1] clamp, 6자리 반올림, 동률 graph 선택 |
| Selective stopping | `core.selective_stop` | 최소 3턴, dialogue 경로, competition 없음, covered 또는 stop·stagnation·gain<.25 |
| 공통 최종 예측 | `prompts.messages('predict')` | 대화+누적 graph JSON, 중심성 점수·중심성 pruning 추가하지 않음 |
| Paired evaluation | `runner.run` | 동일 target/persona의 첫 질문과 실제 첫 응답을 정확히 재사용 |
| Closed-set scoring | `core.score_prediction` | social-role coarse category, 나머지 binary correctness. 한 interest 값의 F1은 binary |
| Majority-normalized Average Gain | `core.majority_baselines`, `score_prediction` | 전체 입력 cohort의 baseline, 차원별 `(score-base)/(1-base)`의 평균 |
| Primary paired statistics | `analyze_recovered`, `paper_audit` | 저장 점수에서 Wilcoxon/BH, 10,000 bootstrap, McNemar/BH 재계산 후 최종 원고 표 대조 |
| 새 결과 비교·비용 | `reporting.py` | AG·차원별 정확도·턴·토큰·gate/graph 비율, 비교 family별 BH |
| 추가 대조군·ablation | `runner.METHODS` | 총 12개 실행 방법; Qwen3-14B common agent, 네 target 설정 제공 |

## 동일성과 재구현의 경계

1. **원 기록**: `data/recorded/`는 제공된 `persona/more`의 복사본입니다. 원 로그·원 통계는 수정하지 않았습니다. primary와 expanded 결과는 다른 비교 family이므로 혼합하지 않습니다.
2. **복구**: 304개 gold profile, 주요 system prompt·schema suffix, 15개 fallback question은 보존 로그에서 복구된 것입니다. cohort의 직렬화·내부 ID는 새로 생성된 것이고 당시 manifest 파일 자체는 아닙니다.
3. **재구현**: Online/Selective 프롬프트, runtime serializer, leakage detector, fuzzy label matching, seed derivation, sampler는 역사적 소스와 완전 동일함이 입증되지 않았습니다. 이 패키지가 해당 누락을 없앴다고 주장하지 않습니다.
4. **보완**: 이전 재구현에서는 selective integrated role이 일반 extract 메시지로 전달됐습니다. 본 패키지는 integrated role에 현재 응답의 node/edge와 grounded competition/discriminator를 함께 요청하는 별도 프롬프트를 사용합니다. 이는 최종 방법에 맞춘 새 프롬프트이며 복구된 과거 프롬프트가 아닙니다.
5. **설정**: Qwen `enable_thinking=False`, 실행 helper의 bf16·context 16,384는 명시적 새 실행 설정입니다. 최종 기록으로 확인되지 않은 과거 설정을 동일하다고 가정하지 않습니다. 모델 revision은 최종 논문에 있는 값을 고정했습니다.
6. **신규 통계**: `summarize`는 선택한 새 run의 paired 결과를 분석합니다. 서로 다른 cohort, 합성/실제 혼합, 중복 target/persona/method, 첫 응답이 다른 pairing은 거부합니다. 전체 네 target을 넣었을 때 primary BH family는 네 검정이며 일부만 넣으면 그 수만큼입니다. 실험 횟수를 persona 수로 늘려 해석하지 않습니다.

## 해석 원칙

최종 논문은 Adaptive의 평균 개선 방향을 관측했지만 모든 target·차원·개별 구성요소의 일관된 유의한 개선을 입증한 것으로 서술하지 않습니다. 특히 random-candidate에 대한 일관된 우위나 Adaptive의 조기 종료 효용을 주장하지 않습니다. Selective의 토큰 절감은 Online 대비이며 더 가벼운 Adaptive 대비 절감으로 바꾸어 설명하지 않습니다. 새 실행의 결과도 이 주장들을 미리 가정하지 않고 평가해야 합니다.
