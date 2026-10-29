# llmops-15-days

A 15-day learning-in-public challenge: fine-tune a small open-source LLM and host it on free or cheap GPUs. One lesson, one commit and one LinkedIn post per day.

**Project thread:** fine-tune a small open model (e.g. Qwen2.5-0.5B/1.5B-Instruct) on text-to-SQL using public data only, then quantize, serve, deploy and monitor it.

**Lifecycle:** data → train → evaluate → quantize → serve → deploy → monitor.

## Compute

Google Colab (T4), Kaggle notebooks, Hugging Face Spaces / ZeroGPU / Inference Endpoints, and pay-per-second options such as Modal, RunPod or Lightning AI. Free-tier limits change, so check them before relying on any.

## Plan

| Day | Topic | Output |
|---|---|---|
| 1 | LLMOps map, setup, base-model inference | Baseline failures noted |
| 2 | Baseline latency and VRAM measurement | Baseline numbers |
| 3 | Dataset prep: cleaning, chat template, split; push to HF Hub | Dataset on the Hub |
| 4 | Eval harness (exact match, execution accuracy); score baseline | `eval/` script + baseline score |
| 5 | LoRA/QLoRA theory; first fine-tune with TRL `SFTTrainer` | First adapter |
| 6 | Hyperparameters (rank, LR, epochs); experiment tracking (W&B) | Run comparison |
| 7 | Re-evaluate tuned model; publish adapter + model card | Before/after table |
| 8 | Merge adapter; quantize (GGUF / AWQ / GPTQ) | Size/speed/accuracy trade-offs |
| 9 | Serve with vLLM (or TGI) | OpenAI-compatible endpoint, throughput numbers |
| 10 | CPU serving with Ollama / llama.cpp | GPU vs CPU comparison |
| 11 | Gradio demo on HF Spaces | Live demo link |
| 12 | FastAPI wrapper: auth, rate limiting, Dockerfile | Containerised API |
| 13 | Monitoring: latency, tokens, errors (Langfuse or Prometheus + Grafana) | Dashboard |
| 14 | CI/CD: GitHub Actions evals gating deploys | Pipeline |
| 15 | Polish, cost table, demo GIF, retrospective | Pinned repo + final post |

Days 5–7 are the most likely to overrun. If so, merge Days 12 and 13.

## Rules

- Public datasets only. No employer or client code, names or data.
- Evals before training. Report real metrics, including failures.
- Save checkpoints to the Hub regularly; free sessions disconnect.

## Daily log

| Day | Date | Commit | Post |
|---|---|---|---|
| 1 | | | |

## Starting each day in a new Claude session

Paste this into a fresh session with this repo attached:

> Continue the llmops-15-days challenge. Read README.md and the latest `notes/` file. Today is Day N. Teach me the concept, give me the hands-on task, then wait for my results. After I paste them, debug with me, commit the day's notes and code, and draft my LinkedIn post from my real numbers.

## Post template

Hook → what I did → result (number or screenshot) → takeaway → tomorrow's teaser. 150–250 words, link to the day's commit.
