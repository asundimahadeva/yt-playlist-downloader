# llm-finetune-to-prod

A 15-day learning-in-public challenge: fine-tune a small open-source LLM, then run it locally on an NVIDIA GTX GPU with Docker and Kubernetes, define the infrastructure with Terraform, and host a demo on free or cheap cloud GPUs. One lesson, one commit and one LinkedIn post per day.

**Project thread:** fine-tune a small open model (e.g. Qwen2.5-0.5B/1.5B-Instruct) on text-to-SQL using public data only, then quantize, serve, containerise, deploy and monitor it.

**Lifecycle:** data → train → evaluate → quantize → serve → containerise → orchestrate (K8s) → provision (Terraform) → monitor.

## Compute

- **Local:** NVIDIA GTX GPU with Docker + NVIDIA Container Toolkit, and a local Kubernetes cluster (kind, minikube or k3s) with the NVIDIA device plugin.
- **Cloud (free or cheap):** Google Colab (T4), Kaggle notebooks, Hugging Face Spaces / ZeroGPU / Inference Endpoints, and pay-per-second options such as Modal, RunPod or Lightning AI. Free-tier limits change, so check them before relying on any.
- **Check your GPU first:** run `nvidia-smi` and note the model and VRAM. QLoRA on a 0.5B–1.5B model typically needs about 6–8 GB. Older GTX cards (Pascal, 10-series) are not supported by vLLM; use llama.cpp for serving on those.
- **Laptop notes:** laptop GTX GPUs often have only 4–6 GB VRAM, so plan to train on Colab/Kaggle and use the laptop for inference, Docker, Kubernetes and Terraform. On Windows, run Docker Desktop with the WSL2 backend and the NVIDIA driver on the Windows side (GPU passthrough works in WSL2). Plug in the charger, use the performance power mode and watch temperatures during long runs.

## Plan

| Day | Topic | Output |
|---|---|---|
| 1 | LLMOps map; verify local GPU, Docker and NVIDIA Container Toolkit; base-model inference | GPU-enabled container running a model |
| 2 | Baseline latency and VRAM measurement | Baseline numbers |
| 3 | Dataset prep: cleaning, chat template, split; push to HF Hub | Dataset on the Hub |
| 4 | Eval harness (exact match, execution accuracy); score baseline | `eval/` script + baseline score |
| 5 | LoRA/QLoRA theory; first fine-tune with TRL `SFTTrainer` (local GPU or Colab/Kaggle) | First adapter |
| 6 | Hyperparameters (rank, LR, epochs); experiment tracking (W&B) | Run comparison |
| 7 | Re-evaluate tuned model; publish adapter + model card | Before/after table |
| 8 | Merge adapter; quantize (GGUF / AWQ / GPTQ) | Size/speed/accuracy trade-offs |
| 9 | Serve in Docker with vLLM (or llama.cpp server on older GPUs); OpenAI-compatible API | Containerised inference server, throughput numbers |
| 10 | Local Kubernetes with GPU: kind/minikube/k3s, NVIDIA device plugin, Deployment + Service for the model | Model served from K8s |
| 11 | Terraform as IaC: namespace, Deployment, Service, config and secrets via the Kubernetes provider; reusable modules | `terraform apply` brings up the stack |
| 12 | FastAPI wrapper (auth, rate limiting) + Gradio demo on HF Spaces | Public demo link |
| 13 | Monitoring: latency, tokens, errors, GPU metrics (Prometheus + Grafana, DCGM exporter, Langfuse) | Dashboard |
| 14 | CI/CD: GitHub Actions runs evals, builds the image and runs `terraform plan` | Pipeline |
| 15 | Polish, cost table, demo GIF, retrospective | Pinned repo + final post |

Days 5–7 and 10–11 are the most likely to overrun. If so, merge Days 12 and 13.

## Rules

- Public datasets only. No employer or client code, names or data.
- Evals before training. Report real metrics, including failures.
- Save checkpoints to the Hub regularly; free sessions disconnect.
- Never commit secrets or Terraform state. Keep `.tfstate`, `*.tfvars` and tokens in `.gitignore`.

## Daily log

| Day | Date | Commit | Post |
|---|---|---|---|
| 1 | | | |

## Starting each day in a new Claude session

Paste this into a fresh session with this repo attached:

> Continue the llm-finetune-to-prod challenge. Read README.md and the latest `notes/` file. Today is Day N. Teach me the concept, give me the hands-on task, then wait for my results. After I paste them, debug with me, commit the day's notes and code, and draft my LinkedIn post from my real numbers.

## Post template

Hook → what I did → result (number or screenshot) → takeaway → tomorrow's teaser. 150–250 words, link to the day's commit.
