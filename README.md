# LLM Client

A minimal Python client that talks to any OpenAI-compatible LLM server (llama.cpp, Ollama, vLLM, etc.) using the `/v1/chat/completions` endpoint.

## Project Structure

```
llm-client/
├── main.py            # Entry point — sends a prompt and prints the response
├── llm_client.py      # LLMClient class (httpx-based)
├── pyproject.toml     # Project metadata & dependencies (uv)
├── .python-version    # Pinned Python version (3.12)
└── requirements.txt   # Dependency list (pip)
```

## Setup

### Option A — uv (recommended)

[uv](https://docs.astral.sh/uv/) manages Python versions, virtual environments, and dependencies in one tool.

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and enter the project
cd llm-client

# Install dependencies (creates .venv automatically)
uv sync

# Run
uv run main.py
```

**Adding a package:**

```bash
uv add httpx          # adds to pyproject.toml + lockfile
```

### Option B — pip

```bash
cd llm-client

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install httpx

# Run
python main.py
```

**Adding a package:**

```bash
pip install <package>
echo "<package>" >> requirements.txt
```

## uv vs pip — Key Differences

| | **uv** | **pip** |
|---|---|---|
| **Speed** | 10–100× faster (Rust-based) | Slower (pure Python) |
| **Config file** | `pyproject.toml` | `requirements.txt` |
| **Lockfile** | `uv.lock` (auto-generated, deterministic) | None (use `pip freeze`) |
| **Virtual env** | Created automatically by `uv sync` / `uv run` | Manual (`python3 -m venv .venv`) |
| **Python version** | Managed via `.python-version` — uv installs it for you | You install Python yourself |
| **Add package** | `uv add httpx` | `pip install httpx` + manually update requirements.txt |
| **Run scripts** | `uv run main.py` (auto-activates env) | `source .venv/bin/activate && python main.py` |

> **TL;DR** — uv does what pip + venv + pyenv do, but faster and with less manual work.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `LLM_MODEL` | ✅ | — | Model name to send in the request (e.g. `qwen2.5`) |
| `LLM_BASE_URL` | — | `http://127.0.0.1:8080/v1` | Base URL of the LLM server |

```bash
# Example
LLM_MODEL=qwen2.5 uv run main.py
```

