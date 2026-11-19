# Cost audit report

상태: **DATA_READY / MANUSCRIPT_EDIT_ONLY**, 단 power, depreciation, cached-token split, 실제 utilization trace는 `[MISSING]`이다.

## Revision 추가 실행 비용

| Bundle | Rows | Model calls | Input tokens | Output tokens | H200 GPU-hours |
|---|---:|---:|---:|---:|---:|
| Main strong-baseline + ablation | 10,944 | 175,104 | 73,516,252 | 28,322,163 | 3.1194 |
| Multi-seed + Qwen3-8B robustness new runs | 1,000 | 16,000 | 6,500,344 | 2,465,908 | 0.6775 |
| Active uncertainty baseline | 1,216 | 43,776 | 19,929,164 | 4,359,337 | 2.3403 |
| **Revision addition total** | **13,160** | **234,880** | **99,945,760** | **35,147,408** | **6.1372** |

Main은 row당 16 calls, active uncertainty는 K=5 repeated prediction 때문에 row당 36 calls다. Robustness row도 16 calls다.

`20260831`의 기존 held-out four-method source는 별도다: 4,864 rows, 87,688 calls, 51,621,229 input tokens, 14,379,336 output tokens. 해당 실행의 신뢰할 수 있는 runtime/GPU-hour log는 현재 패키지에서 찾지 못해 **`[MISSING]`**이다. Revision-addition total에 이 기존 source를 중복 합산하지 않았다.

## Wall-clock과 hardware

- Main eight-shard GPU-time sum: 3.1194 H200 GPU-hours
- Main parallel wave maximum shard elapsed time: 1,548 s
- Active eight-shard GPU-time sum: 2.3403 H200 GPU-hours
- Active parallel wave maximum shard elapsed time: 1,127 s
- Robustness recorded GPU-time sum: 0.6775 H200 GPU-hours
- 전체 job의 queueing과 wave 순서를 포함한 end-to-end wall-clock: **`[MISSING]`**
- Hardware: 8 × NVIDIA H200, 143,771 MiB, driver 580.126.16
- GPU utilization percentage/time-series telemetry: **`[MISSING]`**

GPU-hours는 shard elapsed seconds를 합한 local compute measure다. 전력량이나 탄소량으로 변환하지 않았다.

## Token accounting

- Input: `len(vLLM RequestOutput.prompt_token_ids)`
- Output: `len(vLLM CompletionOutput.token_ids)`
- 각 vLLM model instance가 반환한 native tokenizer 사용
- Cached prompt tokens: backend가 별도 값을 노출하지 않아 분리 기록 **`[MISSING]`**
- Per-cell mean과 persona-bootstrap 95% CI: `results/access_revision/audit/resource_by_cell.csv`
- M1 source Original/Adaptive cost CI: `results/access_revision/existing_runs/cost_summary.csv`

## Monetary cost

- External API inference fee: USD 0; local vLLM inference
- Electricity cost: **`[MISSING]` / not measured**
- Hardware depreciation/amortization: **`[MISSING]` / not measured**
- Facility/cooling/operations cost: **`[MISSING]` / not measured**
- 따라서 USD 0을 전체 computational cost가 0이라는 뜻으로 쓰면 안 된다.

## 근거 파일

- `results/access_revision/audit/resource_and_reproducibility.json`
- `results/access_revision/audit/resource_by_cell.csv`
- `results/access_revision/main/aggregate/runtime_summary.csv`
- `results/access_revision/active_information_gain/main/aggregate/runtime_summary.csv`
- `results/access_revision/main/raw/*/*.jsonl`
- `results/access_revision/robustness/*/raw/*.jsonl`
- `results/access_revision/active_information_gain/main/raw/*/*.jsonl`

## 원고 limitation 문장

> All experiments used local vLLM inference, so the external API fee was USD 0. This value does not imply zero computational cost. We report model calls, native-tokenizer input/output tokens, and H200 GPU-hours, but the backend did not expose cached-token counts separately, and we did not measure power consumption, facility overhead, hardware depreciation, or time-resolved GPU utilization. Accordingly, the reported resource figures should be interpreted as partial compute accounting rather than a complete monetary or environmental cost estimate.

