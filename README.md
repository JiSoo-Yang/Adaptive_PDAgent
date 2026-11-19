# Adaptive PD-Agent: Active Interviewing for LLM Persona Discovery with Bridging Inference

**Adaptive_PDAgent** is an executable software package aligned with the final manuscript supplied in `IEEE_Access_final_main.zip`.

We investigate how an agent can discover a target LLM's persona through **adaptive interviewing**. The agent identifies unresolved dimensions from dialogue, generates three question candidates, and evaluates their coverage and redundancy before selecting the next question or stopping. Response-grounded concepts and **bridging relations** are accumulated in a graph for final persona prediction.

The core **Adaptive** controller selects questions from dialogue alone. **Online** and **Selective** provide comparisons that use graph evidence continuously or selectively. All methods share the dialogue-and-graph final predictor and the exact first question/response for each target–persona pair.

Models:

- **Qwen3-14B** — common agent for questioning, extraction, and prediction.
- **Qwen3-1.7B · Qwen3-4B · Llama-3.2-3B-Instruct · Gemma-3-4B-it** — target models, with revisions pinned in configuration files.

Evaluation data: **304 recovered personas**, each with social role, personality, background, and interests. The package includes preserved experiment records and supports 12 methods with a maximum of five interview turns.

## Repository layout

```text
Adaptive_PDAgent/
├── pdaccess/
│   ├── runner.py                     # Paired interviews and 12 method variants
│   ├── prompts.py                    # Questioning, extraction, and prediction prompts
│   ├── core.py                       # Graphs, selective rules, and persona scoring
│   ├── backend.py                    # Model requests, usage records, and caching
│   ├── reporting.py                  # Statistics and cost analysis for new runs
│   ├── recover.py                    # Recover personas and evidence from recorded logs
│   ├── analyze_recovered.py          # Reanalyze preserved experiment scores
│   └── paper_audit.py                # Compare primary statistics with the final TeX tables
├── config/                           # Schema, prompts, model revisions, and target settings
├── data/recovered/                   # 304 personas and recovered prompt evidence
├── data/recorded/                    # Historical logs and statistical inputs; JSONL via Git LFS
├── paper/                            # Final PDF, TeX, bibliography, and source ZIP
├── tools/                            # Model download, local serving, and connection checks
├── tests/                            # Rules, pairing, HTTP transport, and statistics checks
├── docs/                             # Paper mapping, provenance, and validation scope
├── results/                          # Historical reanalysis and synthetic validation artifacts
├── run.sh                            # CLI wrapper
├── 실행안내.md                       # Detailed installation and execution guide (Korean)
└── 소프트웨어등록.md                 # Software registration description (Korean)
```

## Experiment → paper table map

| Experiment | Paper component | Output | Entry point |
|---|---|---|---|
| Original vs Adaptive | Primary paired comparison | Accuracy, Average Gain, paired tests | `python -m pdaccess run --methods original adaptive ...` |
| Online and Selective | Graph-use and cost comparisons | Gain, tokens, gate activation, graph selection | `python -m pdaccess run --methods original adaptive online selective ...` |
| Additional controls | Random candidate, round robin, dialogue follow-up, generic controller | Paired control comparisons | `--methods adaptive random_candidate round_robin dialogue generic` |
| Ablations and uncertainty control | Candidate/coverage/redundancy ablations and entropy-based selection | Paired diagnostic comparisons | `--methods adaptive direct no_coverage no_redundancy uncertainty` |
| New-run analysis | Statistical and cost reporting | CSV tables and `report.json` | `python -m pdaccess summarize <run> --output <report>` |
| Historical score audit | Final manuscript primary comparison tables | Recalculated statistics and table agreement checks | `python -m pdaccess audit-paper --output <audit>` |

See the [paper-to-code mapping](docs/PAPER_MAPPING.md) for implementation details and reconstruction boundaries. Historical reanalysis and new model inference are separate execution paths.

## Requirements

Linux and Python 3.11+. Data checks and synthetic interviews use the Python standard library. Statistical analysis requires **NumPy 2.2.6 and SciPy 1.17.1**. Actual interviews use local **vLLM 0.11.0** servers in a separate CUDA environment.

Install Git LFS before cloning to retrieve the preserved experiment records:

```bash
git lfs install
git clone https://github.com/JiSoo-Yang/Adaptive_PDAgent.git
cd Adaptive_PDAgent
git lfs pull

python3 -m venv .venv-analysis
.venv-analysis/bin/python -m pip install -r requirements-analysis.txt
```

Basic checks and a synthetic interview without GPU inference:

```bash
.venv-analysis/bin/python -m pdaccess doctor
.venv-analysis/bin/python -m unittest discover -s tests -v
.venv-analysis/bin/python -m pdaccess run \
  --manifest data/recovered/cohort_for_reimplementation.json \
  --config config/qwen1_7b.json --mock --limit 2 \
  --output results/my_smoke
```

Recalculate the preserved primary scores against the final manuscript:

```bash
.venv-analysis/bin/python -m pdaccess audit-paper \
  --output results/my_paper_audit
```

For actual interviews, install `requirements-serving.txt` in a separate environment, download the agent and target models, and start both servers. The [execution guide](실행안내.md) contains the complete commands for downloads, server startup, pilot interviews, all four targets, and combined statistical analysis.

## Inputs (bundled and external)

- **Bundled personas**: `data/recovered/cohort_for_reimplementation.json` supplies the 304-persona evaluation cohort.
- **Bundled records**: `data/recorded/` preserves historical experiments and score inputs. Approximately 1.2 GB of JSONL data is distributed through Git LFS; a GitHub ZIP download may contain pointers instead of the data.
- **Bundled manuscript**: `paper/` contains the final paper and source used for method mapping and the primary-table audit.
- **External model weights**: obtain them using `tools/download_models.py`; revisions and local paths are defined in `config/models.json`. Llama and Gemma require an account with the appropriate model access.
- **Runtime configuration**: use `config/qwen1_7b.json`, `config/qwen4b.json`, `config/llama3b.json`, or `config/gemma4b.json` for the selected target.

New interviews write `results.jsonl`, `summary.json`, request records, configuration, and source snapshots into the chosen run directory. `summarize` produces method metrics, paired tests, dimension tests, and selective diagnostics in a separate report directory.

## Notes

- This package is a **manuscript-based reconstruction**, not the complete historical experiment source. Major prompts and persona profiles were recovered from logs; some Online/Selective prompts, label matching, serialization, and seed derivation are reconstructed. The integrated Selective extraction/state prompt was explicitly revised for this package.
- Adaptive question selection uses dialogue without a host-side weighted ranking. Selective uses the documented actionability gate and utility rules. Neither graph benefit nor superiority of every component is assumed in advance.
- Historical reanalysis passed **40 primary-table checks** at the manuscript's printed precision. The package also passed **14 tests** and a **24-interview synthetic check** covering all 12 methods. These checks do not establish fresh model reproduction.
- Model weights were **not downloaded**, and GPU inference was **not executed during package preparation**. Synthetic runs are marked separately and are not model-performance evidence. See [validation](docs/VALIDATION.md).
- Use a new output directory for a new experiment. Add `--resume` only when continuing an interrupted run with the same configuration and inputs. Include all four targets in a combined report to match the primary four-test BH correction family.
- The [software registration description](소프트웨어등록.md) and [execution guide](실행안내.md) are maintained separately in Korean.
