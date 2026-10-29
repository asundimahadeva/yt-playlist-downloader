# Handoff: llm-finetune-to-prod (for your local Claude environment)

Paste this file into a local Claude Code session, together with `README.md` from this folder.

## Goal
Post on LinkedIn every day for 15 days while learning LLMOps: fine-tune a small open model, then host it on free or cheap GPUs. Claude is the tutor and pair-programmer. Each day starts in a new session: Claude teaches a concept, gives a hands-on task, you run it and paste results, Claude debugs, commits notes and code, and drafts the LinkedIn post from your real numbers.

## Decisions so far
- GitHub login: `asundimahadeva`. Location: Bangalore.
- Repo name: `llm-finetune-to-prod` (recommended, not yet confirmed). Alternatives: `llmops-from-scratch`, `text2sql-finetune-serve`, `open-llm-ops-journey`.
- Repo description: "Fine-tune an open-source LLM with QLoRA and host it on free GPUs: data, training, evals, quantization, serving, deployment and monitoring. 15-day learning in public."
- Topics: `llmops`, `fine-tuning`, `qlora`, `huggingface`, `vllm`, `text-to-sql`, `learning-in-public`, `mlops`.
- Hardware: NVIDIA GTX laptop GPU, probably 4-6 GB VRAM. Train on Colab or Kaggle. Use the laptop for inference, Docker, Kubernetes (kind, minikube or k3s) and Terraform. On Windows use Docker Desktop with the WSL2 backend and the NVIDIA driver on the Windows side.
- vLLM does not support Pascal (10-series) GPUs, so use llama.cpp or Ollama there.
- Project thread: fine-tune Qwen2.5-0.5B/1.5B-Instruct on text-to-SQL (dataset `b-mc2/sql-create-context`), public data only.
- Lifecycle: data, train, evaluate, quantize, serve, containerise, orchestrate (K8s), provision (Terraform), monitor.

## The plan
The full 15-day table, rules and post template are in `README.md` in this folder.

## Day 1 task (not yet run)
1. Run `nvidia-smi` and note the GPU model and VRAM. Verify Docker and the NVIDIA Container Toolkit.
2. Create a free Hugging Face account and a write token, and an empty public GitHub repo.
3. In Colab (T4) or locally:

```python
!pip install -q transformers accelerate
```
```python
from transformers import pipeline

pipe = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", device_map="auto")

schema = "CREATE TABLE employees (id INT, name TEXT, dept TEXT, salary INT);"
question = "Which departments have an average salary above 70000?"
messages = [
    {"role": "system", "content": "You write SQLite SQL. Reply with SQL only."},
    {"role": "user", "content": f"{schema}\n\nQuestion: {question}"},
]
print(pipe(messages, max_new_tokens=100)[0]["generated_text"][-1]["content"])
```

4. Try 3-5 more questions, including a join and a GROUP BY. Note the failures as the baseline.
5. Report back: the model outputs, `nvidia-smi` memory use and any errors.

## Day 1 LinkedIn draft
Announce the 15-day challenge and the pipeline "data -> fine-tune (QLoRA) -> evaluate -> quantize -> serve -> deploy -> monitor". Then: "Day 1: I ran a 0.5B-parameter model on text-to-SQL, with no training. It got [X] of [Y] questions right. Typical failure: [your example]." Hashtags: #LLMOps #FineTuning #HuggingFace #LearningInPublic

## Pending
1. Create the empty public repo `llm-finetune-to-prod` (the cloud session could not create it: 403, access is scoped to `yt-playlist-downloader`). Copy `README.md` into it.
2. Once the standalone repo is live, delete the staging folder `llmops-15-days/` from the `yt-playlist-downloader` branch `claude/wizardly-einstein-haefiw`.
3. Share your `nvidia-smi` output and OS (Windows or Linux; macOS has no NVIDIA support).
4. To work on your PC, run `claude remote-control` in the project folder, or use the Claude Desktop app.

## Starting prompt for each new day
> Continue the llm-finetune-to-prod challenge. Read README.md and the latest `notes/` file. Today is Day N. Teach me the concept, give me the hands-on task, then wait for my results. After I paste them, debug with me, commit the day's notes and code, and draft my LinkedIn post from my real numbers.
