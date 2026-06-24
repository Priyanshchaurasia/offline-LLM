# Offline Coding LLM (DeepSeek-Coder 1.3B)

A lightweight, offline coding assistant built on **DeepSeek-Coder 1.3B**, served locally through **Ollama** and exposed via a **FastAPI** backend with a simple frontend. Once set up, inference runs entirely on your own machine — no internet required.

> **Note on weights:** The model file (`coding-model.gguf`, ~2.5 GB) and the base model are **not** included in this repo due to size. See [Setup](#setup) to supply them locally.

---

## Features

- Runs offline at inference time
- Based on DeepSeek-Coder 1.3B (small, lightweight)
- FastAPI backend with streaming responses
- Custom fine-tuning pipeline included
- Tuned for coding tasks (low temperature, code-focused system prompt)

---

## Repository structure

```
.
├── prepare_dataset.py     # Downloads & saves the training dataset locally
├── create_modelfile.py    # Generates the Ollama Modelfile
├── Modelfile              # Ollama model definition (points to the .gguf weights)
├── main.py                # FastAPI backend exposing /chat (streaming) and /health
├── frontend/              # User interface
├── requirements.txt       # Python dependencies
└── README.md
```

**Not included (kept local):**
- `coding-model.gguf` — fine-tuned weights (~2.5 GB)
- `deepseek-coder-1.3b/` — base model files
- `coding_dataset/` — saved training data

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running (serves on `http://localhost:11434`)
- A GGUF model file (your `coding-model.gguf`)

```bash
pip install -r requirements.txt
```

---

## Setup

1. **Install Ollama** from https://ollama.com and make sure it is running.

2. **Place your model weights.** Put `coding-model.gguf` where the Modelfile expects it. The included `create_modelfile.py` generates a Modelfile with an absolute Windows path:

   ```
   FROM C:/Users/priya/OneDrive/Desktop/ONGC/coding-model.gguf
   ```

   **Edit this path** in `create_modelfile.py` to match where you keep the file, then regenerate the Modelfile:

   ```bash
   python create_modelfile.py
   ```

3. **Register the model with Ollama:**

   ```bash
   ollama create coding-model -f Modelfile
   ```

   > **Heads up — model name mismatch.** The Modelfile registers the model as `coding-model`, but `main.py` currently calls `deepseek-coder:1.3b` (the base model). Pick one:
   > - To use your **fine-tuned** model, change the `model` field in `main.py` to `coding-model`, **or**
   > - To use the **base** model, pull it with `ollama pull deepseek-coder:1.3b` and skip the custom Modelfile.

4. **Start the backend:**

   ```bash
   uvicorn main:app --reload
   ```

   The API runs at `http://localhost:8000`:
   - `POST /chat` — send `{"message": "..."}`, receives a streamed text response
   - `GET /health` — returns `{"status": "ok"}`

5. **Open the frontend** in `frontend/` and point it at `http://localhost:8000/chat`.
   <!-- CONFIRM: add the exact command to launch your frontend -->

---

## Training / fine-tuning

The fine-tuning data comes from the public `iamtarun/python_code_instructions_18k_alpaca` dataset.

1. **Download and cache the dataset** (requires internet **this step only**):

   ```bash
   python prepare_dataset.py
   ```

   This saves the data to `./coding_dataset` so later steps work offline.

2. Build the Modelfile and create the model (see [Setup](#setup) steps 2–3).

---

## Model parameters

The Modelfile configures the model for focused, deterministic coding output:

- `temperature 0.2` — low randomness, more consistent code
- `top_p 0.95`
- `repeat_penalty 1.1`
- `num_ctx 2048` — context window
- System prompt restricts it to programming/software tasks

---

## License

See [LICENSE](LICENSE).
