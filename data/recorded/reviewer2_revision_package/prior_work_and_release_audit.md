# Prior-work and release audit

상태: **PARTIAL / MANUSCRIPT_EDIT_REQUIRED / EXTERNAL_RELEASE_ACTION_REQUIRED**. 이전 ICPR 논문은 확인했지만 현재 Access 원고, `.bib`, preprint inventory와 permanent release가 없다.

## 확인 가능한 source

| Item | 경로/식별자 | 상태 |
|---|---|---|
| 이전 ICPR 논문 PDF | `docs/papers/ICPR_2026_persona_camera_ready__유료_.pdf` | 존재 |
| Reviewer decision | `IEEE Access - Decision on Manuscript ID Access-2026-38546.pdf` | 존재; M10/m1/m7/m8 요구의 근거 |
| 현재 Access manuscript source/PDF | `[MISSING]` | 문장 단위 reuse diff를 수행할 수 없음 |
| Bibliography `.bib` | `[MISSING]` | preprint 목록과 citation key를 감사할 수 없음 |
| Git remote | `https://github.com/JiSoo-Yang/Persona_Bridging_Access.git` | mutable repository URL |
| 현재 확인한 local HEAD | `2f98390b0dc2b29fe693ae30ee9e7e2483cbeb4e` | 2026-07-07 commit; revision 결과를 가리키는 permanent release라는 증거 없음 |
| Git tag | `[MISSING]` | local tag 없음 |
| GitHub release | `[MISSING]` | 작업공간에 release identifier 없음 |
| DOI/Zenodo record | `[MISSING]` | 작업공간에 permanent identifier 없음 |

## 표현·문장·결과 재사용 inventory

현재 manuscript source가 없어 Access 원고와 ICPR PDF 사이의 exact textual overlap, table-entry overlap, reused method prose와 illustration 목록은 **`[MISSING]`**이다. 임의의 유사도를 산출하지 않았다.

Reviewer decision으로 확인되는 최소 범위는 다음과 같다.

| Reuse area | 확인된 문제 | 필요한 공개/수정 | 현재 상태 |
|---|---|---|---|
| Table 3 | Reviewer는 이전 ICPR 결과가 재현돼 있다고 지적 | 각 row/cell이 그대로 reproduced, recomputed, 또는 adapted되었는지 표시 | `[MISSING]`; current manuscript/table caption 없음 |
| Method identity | `PD-Agent (Ours)`는 이전 방법과 새 기여의 경계를 흐림 | `Original PD-Agent [4]`로 변경 | **MANUSCRIPT_EDIT_REQUIRED** |
| Previously Published Statement | “shares no results/tables/figures” 취지와 Table 3 reuse가 모순된다는 지적 | 실제 reused/adapted result, table, text, method, illustration을 열거하고 statement를 일치시킴 | **MANUSCRIPT_EDIT_REQUIRED** |
| “re-examined using the per-dimension protocol” | Table 3가 과거 cosine 값을 보고한다면 문구가 무엇을 뜻하는지 불명확 | 어떤 값이 과거 값이고 어떤 값이 현 평가 코드로 재계산됐는지 cell 단위로 설명 | `[MISSING]`; source manuscript와 provenance mapping 필요 |
| Method text/equations | exact reuse 여부 | source sentence/equation, prior location, current location, verbatim/adapted 여부를 inventory | `[MISSING]` |
| Illustrations | exact reuse 여부 | figure별 reused/adapted/new와 permission/licence 여부 기록 | `[MISSING]` |

## Table 3 수정 요구

1. Prior-work 중심이면 main text에서 supplementary로 이동한다.
2. Caption 또는 첫 note에 이전 ICPR 연구와의 관계를 밝힌다.
3. `PD-Agent (Ours)`를 `Original PD-Agent [4]`로 바꾼다.
4. 각 수치에 `reported previously`, `recomputed from prior raw outputs`, `new Access experiment` 중 정확한 provenance를 붙인다. 현재 provenance별 cell 목록은 `[MISSING]`이다.
5. 과거 cosine metric과 현재 per-dimension raw metric/normalized gain을 한 열에서 혼용하지 않는다.
6. 현재 local 후보 `results/selective_gai/table_main_rows.tex`는 caption/provenance가 없으므로 이 요구를 충족한 최종 Table 3로 볼 수 없다. `results/tables/table3_rows.tex`는 파일에 incomplete 표시가 있어 사용하면 안 된다.

제안 caption 방향:

> Supplementary comparison with Original PD-Agent [4]. Entries reproduced or recomputed from the prior study are identified explicitly; all newly collected Adaptive PD-Agent results are labeled as new experiments in this work.

어떤 entry가 reproduced/recomputed/new인지 확정할 source mapping은 `[MISSING]`이므로 위 문장을 그대로 넣기 전에 cell provenance를 채워야 한다.

## Preprint/reference audit

- Current `.bib`: `[MISSING]`
- Manuscript에서 인용한 preprint 전체 목록: `[MISSING]`
- 각 preprint의 peer-reviewed version 상태: `[MISSING]`
- 갱신해야 할 DOI/venue/year/page: `[MISSING]`
- Last checked date와 검색 기준: `[MISSING]`

이는 **EXTERNAL_LITERATURE_CHECK_REQUIRED** 항목이다. 원고와 bibliography가 들어온 뒤 citation key별로 title/author를 대조하고 공식 publisher 또는 DOI record에서 publication status를 확인해야 한다.

## Code release/DOI audit

현재 raw-data manifest와 SHA-256은 각 결과 폴더에 있지만, 이는 외부의 immutable archive가 아니다. Reviewer m7을 충족하려면 다음 external action이 필요하다.

1. 최종 원고 수치와 대응하는 source/data commit을 확정한다.
2. 그 commit에 version tag를 만들고 GitHub release 또는 동등한 immutable release를 발행한다.
3. Zenodo 또는 동등한 archive로 DOI를 발급한다.
4. Release에 code, configs, frozen persona manifest, aggregate CSV, 생성 스크립트와 checksum을 포함한다. 모델 라이선스로 배포할 수 없는 checkpoint는 exact model identifier와 revision만 기록한다.
5. 원고의 Data/Code Availability와 response letter에 tag, commit, release URL, DOI를 동일하게 쓴다.

현재 채울 수 없는 release metadata:

| Field | Value |
|---|---|
| Release tag | `[MISSING]` |
| Release commit | `[MISSING]` |
| Published release URL | `[MISSING]` |
| DOI | `[MISSING]` |
| Archive publication date | `[MISSING]` |
| License/version | `[MISSING]` |

이 보고서는 외부 publish 작업을 수행하지 않았다. Reviewer 대응을 위해서는 **EXTERNAL_RELEASE_ACTION_REQUIRED**다.

## 원고용 disclosure 방향

정확한 reuse inventory가 완성된 뒤 Previously Published Statement는 최소한 다음 내용을 포함해야 한다.

> This submission extends Original PD-Agent [4] with an LLM-prompted adaptive interviewing policy and new held-out evaluations. Table [MISSING] is retained only as a clearly labeled prior-work comparison. The table notes identify which entries were reported previously, recomputed from prior outputs, or generated in the present study; no newly claimed Adaptive results are presented as prior-work results.

현재 reuse cell 목록과 table number가 `[MISSING]`이므로 이 문장은 구조적 초안이며 final factual statement가 아니다.
