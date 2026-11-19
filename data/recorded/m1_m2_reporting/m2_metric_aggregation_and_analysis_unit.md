# M2 metric aggregation and analysis unit report

## 분석 단위의 구분

| 수준 | 관측 단위 | 산출값 | 통계적 사용 |
|---|---|---|---|
| Persona level | 하나의 target model, 하나의 persona, 하나의 method | dimension score, majority-normalized gain, Average Gain | Original과 Adaptive를 같은 persona index로 pair해 Wilcoxon 또는 McNemar에 입력 |
| Cohort level | 한 target-method cell의 304 personas 전체 | accuracy, macro-F1, micro-F1, MAE, Spearman correlation, mean gain | 기술통계와 표의 cell summary로 사용. 단일 cohort scalar를 304개 관측값으로 복제하지 않음 |

M1의 독립 관측 단위는 target별 **persona pair**다. 각 target에 304개의 pair가 있고 target 간에는 별도 검정을 수행했다.

## Persona-level dimension score

Persona `i`, method `m`, dimension `d`의 점수를 `s_(i,d)^(m)`이라 한다.

| Dimension | M1 persona-level score | 현재 원자료의 값 |
|---|---|---|
| Social role | predicted specific role과 gold specific role을 각각 3개 coarse category로 변환한 뒤 category가 같으면 1, 아니면 0 | 0/1 |
| Personality | 해당 gold Big-Five trait의 yes/no value가 정확히 같으면 1, 아니면 0 | 0/1 |
| Background | 해당 gold background category 안의 value가 정확히 같으면 1, 아니면 0 | 0/1 |
| Interests | gold/predicted value set의 per-persona set F1 | 현재 schema와 2,432개 M1 원자료에서는 gold와 prediction이 모두 singleton이므로 0/1 |

Social role의 specific-role accuracy와 macro-F1, background의 category agreement 등은 보조 cohort 지표다. M1 Average Gain의 social-role 성분은 coarse-category correctness이고 background 성분은 value exactness다.

## Cohort-level dimension metric

저장된 `evaluation/metrics.py`는 304개 scored record를 모아 다음 기술통계를 계산한다.

- Social role: specific-role top-1 accuracy, specific-role macro-F1, coarse-category accuracy. Primary cohort metric은 coarse-category accuracy다.
- Personality: yes/no accuracy, macro-F1, binary MAE, Spearman correlation, trait별 accuracy. Primary cohort metric은 accuracy다.
- Background: value accuracy, predicted-category agreement, value macro-F1, category별 accuracy. Primary cohort metric은 value accuracy다.
- Interests: exact match, pooled micro-F1, persona F1의 평균인 macro-F1, mean Jaccard. Primary cohort metric은 pooled micro-F1이다.

Interests의 cohort micro-F1은 모든 persona의 set prediction을 합쳐 다음처럼 계산한다.

`micro-F1 = 2TP / (2TP + FP + FN)`

현재 held-out M1 자료에서는 각 gold와 prediction이 모두 하나의 문자열 label이며 모든 parsing이 성공했다. 따라서 persona-level interest F1은 모두 0 또는 1이고, 이 자료에 한해 pooled micro-F1은 interest exact accuracy 및 persona F1 평균과 수치적으로 같다. 이 동치는 singleton schema에 따른 것이며 일반적인 multi-label 데이터에는 성립하지 않는다.

## Majority baseline

모든 baseline은 frozen held-out 304 personas의 gold label만으로 한 번 계산하며 method나 target에 따라 다시 계산하지 않는다. 문자열 비교에는 저장된 normalization을 적용한다.

### Social role

각 specific role을 `professional`, `technical_management`, `general_role` 중 하나로 변환한다. 전체 304명에서 가장 많은 coarse category인 `professional`을 항상 예측하는 정확도가 baseline이다.

`B_social = 118 / 304 = 0.3881578947`

### Personality, background, interests

이 세 dimension은 category/trait별 label space가 다르므로 조건부 majority를 사용한다. Persona `i`의 group을 `g_i`라 하고, 같은 group의 gold value 중 최빈값을 `mode(g_i)`라 하면:

`B_d = (1/N) Σ_i I[y_(i,d) = mode(g_i)]`, `N = 304`

- Personality: Big-Five trait별 yes/no majority. `166/304 = 0.5460526316`
- Background: background category별 value majority. `84/304 = 0.2763157895`
- Interests: interest category별 value majority. `78/304 = 0.2565789474`

실제 conditional majority label은 `majority_baselines.csv`와 `manifest.json`에 보존했다. 예를 들어 personality는 openness/conscientiousness/agreeableness/neuroticism에서 `no`, extroversion에서 `yes`다.

## Majority-normalized gain

Persona `i`, method `m`, dimension `d`에 대해:

`G_(i,d)^(m) = (s_(i,d)^(m) − B_d) / (1 − B_d)`

- Correct score `s=1`이면 gain은 1이다.
- Incorrect score `s=0`이면 gain은 `−B_d/(1−B_d)`다.
- 304명 평균 score가 baseline과 같으면 해당 dimension의 평균 gain은 0이다.

## 네 dimension의 Average Gain

각 persona의 Average Gain은 네 dimension gain의 동일 가중 산술평균이다.

`AG_i^(m) = (G_(i,social)^(m) + G_(i,personality)^(m) + G_(i,background)^(m) + G_(i,interests)^(m)) / 4`

Target-method cell의 보고용 Average Gain은 persona-level Average Gain의 평균이다.

`mean_AG^(m) = (1/304) Σ_i AG_i^(m)`

가중치 학습, dimension별 표본수 가중, micro averaging은 사용하지 않았다.

## Wilcoxon에 들어간 정확한 관측값

Target `t`마다 다음 304개 값을 만든다.

`Δ_(t,i) = AG_(t,i)^(Adaptive) − AG_(t,i)^(Original)`, `i = 0, …, 303`

Wilcoxon 입력 vector는 `[Δ_(t,0), …, Δ_(t,303)]`이다. 동일 persona의 두 method 결과를 먼저 빼므로 paired 설계가 보존된다. Zero difference는 SciPy의 `zero_method='wilcox'`에 의해 signed-rank 계산에서 빠지지만 +/−/tie 표와 전체 `N=304`에는 남는다.

각 `AG`와 `Δ`의 full-precision 값은 `m1_persona_level.csv`에 있다.

## Cohort micro-F1의 paired test 처리

Cohort-level interest micro-F1은 하나의 target-method cell당 scalar 하나이므로 M1 Wilcoxon의 독립 관측값으로 직접 사용하지 않았다. 특히 같은 micro-F1 하나를 304개 persona 관측값으로 복제하지 않았다.

Paired inference는 다음처럼 처리했다.

1. Average Gain Wilcoxon: 각 persona의 interest set F1을 나머지 세 persona-level score와 함께 정규화하고 평균한 `AG_i`를 사용했다.
2. Dimension-level test: 각 persona의 Original/Adaptive interest correctness pair를 exact McNemar에 사용했다. 현재 singleton 자료에서 interest F1이 0/1이므로 이 binary pair가 정의된다.
3. Cohort micro-F1: 표에 기술통계로 보고하되, 그 자체에 304개 독립 관측값이 있는 것처럼 검정하지 않았다.

원고에는 “micro-F1을 persona별 독립 관측값으로 사용했다”는 표현을 쓰면 안 된다. 정확한 표현은 “the cohort micro-F1 was reported descriptively, whereas paired inference used persona-level singleton-set F1/correctness and persona-level Average Gain”이다.

