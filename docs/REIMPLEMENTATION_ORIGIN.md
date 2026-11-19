# Access PD-Agent: recovered evidence and reconstruction

This is a **new implementation**, not the missing historical `evaluation/` source tree.
It does not modify `final_revision`, the legacy `code` repository, or supplied `more` records.

## What was recovered

`../more/` contains 13,160 raw inference records: 10,944 expanded main runs, 1,216 active-uncertainty runs, and 1,000 robustness runs. Recorded calls contain actual `prompt_messages`, raw responses, decoding settings and seeds. Separate primary-run CSVs contain 9,728 dimension-score rows.

The extraction in `../recovered_access_artifacts/` provides:

- 304 historical persona identities and ground-truth profiles;
- verbatim, provenance-linked call examples and system prompts;
- all 15 observed fallback-question slots (four dimensions plus generic, three indices each), with consistent mappings across 3,041 replacement events;
- source-file hashes and call-role inventories;
- a cohort converted for this runner, preserving historical source IDs separately from new internal IDs.

`../recovered_access_artifacts/statistics/primary_reanalysis.json` reproduces the primary effect estimates, Wilcoxon statistics, raw/BH p-values, bootstrap interval endpoints, direction counts, and dimension-level McNemar/BH results **exactly** against the saved reports. This is reanalysis of recorded scores, not new model inference or independent recovery of the historical label scorer.

## Install and test

Core sampling, rules, HTTP execution, log recovery, and synthetic tests use Python 3.11+ standard library. Statistical reanalysis additionally needs:

```bash
python -m pip install -r requirements-analysis.txt
python -m unittest discover -s tests -v
```

No OpenAI account or hosted API is required. The client targets local vLLM-compatible servers. Existing `.env` files are not read or copied.

## Prefer recovering and reanalyzing the historical evidence

Run from this directory. Use a new output path; commands refuse to overwrite results.

```bash
python -m pdaccess recover ../more ../recovered_access_artifacts_v2
python -m pdaccess analyze-recorded ../more ../recovered_access_artifacts/statistics_recheck
python -m pdaccess import-cohort \
  ../recovered_access_artifacts/historical_personas.jsonl \
  historical_cohort.json
```

`recover` traverses raw JSONL without changing it and validates first-turn pairing within each run family/target/persona/seed. It checks the supplied main-file and primary-report checksums. The original persona JSONL byte stream is not recovered; exported persona records have new serialization with historical IDs and evidence references.

The additional `observed_fallback_bank_mapping.json` was derived by associating replaced questions with the preceding decision's dimension (or the active baseline's uncertainty dimension) and `(turn - 1) % 3`. Its 15 slots each contain exactly one observed string. This is observational recovery, not recovery of the source-code definition.

## Inspect or rerun an actual recorded model request

```bash
python -m pdaccess replay \
  --example ../recovered_access_artifacts/call_examples/example_000.json \
  --output inspected_request.json
```

Without `--execute`, this only writes the recorded request and response for inspection.
To send the exact recorded messages and recorded sampling parameters to a locally served corresponding model:

```bash
python -m pdaccess replay \
  --example ../recovered_access_artifacts/call_examples/example_000.json \
  --base-url http://127.0.0.1:8000/v1 \
  --execute --output new_inference_from_recorded_request.json
```

Checkpoint revisions, tokenizer/chat-template settings, backend version and hardware must be checked independently. The HTTP API cannot certify which revision was loaded. A recorded seed does not guarantee a byte-identical response across environments. Responses from a rerun are new results.

## Run the reconstructed interview pipeline

A synthetic smoke check requires no models:

```bash
python -m pdaccess run \
  --manifest ../recovered_access_artifacts/cohort_for_reimplementation.json \
  --mock --limit 2 --output smoke_new
```

Synthetic runs are marked `synthetic_smoke_only`, have no fabricated token counts, and must not be treated as experimental results. A 24-interview plumbing check (2 personas × 12 methods) was executed; its synthetic output folder was removed during cleanup. Tests remain available.

For a new cohort, distinct from the recovered historical values:

```bash
python -m pdaccess manifest --count 100 --seed 20260801 --output development_new.json
python -m pdaccess manifest --count 304 --seed 20260802 \
  --exclude development_new.json --output heldout_new.json
```

The sampler and seed derivation are newly implemented. Supplying the historical seed alone does not reproduce the original cohort. Baselines are computed from the entire input manifest, even when `--limit` runs only a small pilot. A baseline of one makes AG undefined (`null`), rather than producing a misleading number.

For local GPU inference, install vLLM in a separate environment and serve agent and target on separate ports. For example, in two terminals on suitable GPUs:

```bash
CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3-14B \
  --revision 40c069824f4251a91eefaf281ebe4c544efd3e18 \
  --dtype bfloat16 --generation-config vllm --port 8000

CUDA_VISIBLE_DEVICES=1 vllm serve Qwen/Qwen3-1.7B \
  --revision 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e \
  --dtype bfloat16 --generation-config vllm --port 8001
```

Use vLLM 0.11.0 for the reported backend version; installation/GPU compatibility was not tested here. `config/run.json` holds the checkpoint IDs, endpoints, budget and explicit reconstruction choices. It specifies `enable_thinking=False` for Qwen, which has not been verified as a historical setting. Change model, revision and applicable chat-template settings together for another target.

```bash
python -m pdaccess run \
  --manifest ../recovered_access_artifacts/cohort_for_reimplementation.json \
  --config config/run.json --limit 2 \
  --methods original adaptive --output pilot_actual
```

The full registry is `original adaptive online selective random_candidate round_robin dialogue generic direct no_coverage no_redundancy uncertainty`. A run without `--limit` processes the entire manifest. Do not run a full experiment until inspecting the pilot calls, model settings and remaining reconstruction differences.

The client follows the [vLLM 0.11.0 OpenAI-compatible serving API](https://docs.vllm.ai/en/v0.11.0/serving/openai_compatible_server.html). If a local server needs authentication, set `VLLM_API_KEY`; it is not persisted in call records.

## Provenance and remaining differences

| Component | Status |
|---|---|
| Initial, Original, Adaptive, dialogue, generic and ablation prompt wording | System text and schema suffixes recovered from actual calls; representative complete message reconstruction tested |
| Extraction and final prediction | Recovered instructions/schema; graph-state serialization remains reconstructed |
| Fallback questions | 15 strings and dimension/index mappings recovered observationally |
| Adaptive selection | LLM-selected question; no invented host-side weighted ranking or score tie-break |
| Graph validation and canonicalization | Reimplemented manuscript rules; not regression-validated against every recorded graph update |
| Online/Selective | Manuscript-based implementation; full historical prompt/call logs not found in supplied raw files |
| Uncertainty selection | Five stochastic predictions, temperature 0.8, entropy/least-asked/fixed-order selection; targeted question generation uses the reconstructed interface |
| Gold persona values | Recovered 304 historical profiles; new manifest serialization/internal IDs |
| Initial pairing | Exact reuse across methods in a new run; historical initial responses are not automatically substituted |
| Label canonicalizer, leakage filtering, seed derivation | Newly implemented; exact old source not recovered |
| Main/expanded statistics | Historical primary inputs reanalyzed separately; new pilot scores are not historical results |

Do not relabel this code as the original experiment implementation. In particular, passing offline tests does not establish model-level equivalence or reproduce the published predictions. Newly generated results must remain separate from the recorded primary and expanded runs.

## Audit and restart behavior

Each run records configuration, code fingerprint, prompt examples, actual requests/responses, seeds, usage returned by the server, method decisions and graph rejection counts. The JSONL results contain ground truth only for evaluation; controller/predictor messages do not receive gold values. Target persona values appear only in the private target system prompt.

`--resume` permits continuation only with unchanged source/config/manifest/method selection. Successfully cached calls are reused; existing successful persona-method rows are not repeated. Transport errors stop the run, rather than silently excluding personas. Malformed controller JSON follows the documented parser/fallback path.

Per-method token totals attribute shared initial calls to each paired method. Physical model calls must instead be counted by unique cached call IDs; replay/cache hits do not consume new model calls. Missing server usage is reported as unknown.
