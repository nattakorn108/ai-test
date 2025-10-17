## AI Test – LLM Benchmark Toolkit

A small Python utility and shell script to benchmark local LLMs served by Ollama. The Python script runs the `llm_benchmark run` workflow and pretty-prints results in a table. The shell script performs a quick latency and throughput check for a single prompt using Ollama's HTTP API.

### Features
- Checks if the Ollama server is running before benchmarking.
- Executes `llm_benchmark run` and parses output into a rich table.
- Provides a simple `benchmark.sh` to measure latency and tokens-per-second (TPS) for a single prompt.

### Requirements
- Python 3.9+
- Ollama running locally (`http://localhost:11434`)
- System tools for the shell script: `curl`, `jq`, and `bc`

### Installation
```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage
#### Python benchmark (rich table)
Runs the official `llm-benchmark` suite and renders a readable table.
```bash
python main.py
```
- The script will check if Ollama is running.
- If the `llm-benchmark` command is unavailable, install it: `pip install llm-benchmark`.
- If your Ollama version is outdated for the selected models, update via the Ollama downloads page.

#### Quick latency/TPS check (shell script)
Benchmarks a single prompt against a model via Ollama's HTTP API.
```bash
bash benchmark.sh
```
Environment variables you can set before running:
- `MODEL` (default: `llama3`)
- `PROMPT` (default: `Why is the sky blue?`)

Example:
```bash
MODEL=llama3.1 PROMPT="Explain diffusion models in 1 paragraph" bash benchmark.sh
```

### Project Structure
```text
.
├── main.py           # Runs llm-benchmark and prints a rich table
├── benchmark.sh      # Quick latency and TPS benchmark via Ollama API
├── requirements.txt  # Python dependencies (llm-benchmark, requests, rich)
├── .gitignore        # Python, env, and sensitive files ignored
└── README.md         # This file
```

### Troubleshooting
- Ollama not running: Start Ollama so `http://localhost:11434` is reachable.
- `llm-benchmark` not found: `pip install llm-benchmark` (inside your venv if using one).
- Outdated Ollama for model downloads: upgrade Ollama to the latest version.
- Shell script missing tools: install `curl`, `jq`, and `bc` via your OS package manager.

### Notes
- `.env` and other dotenv files, as well as common sensitive keys (e.g., `*.pem`, `id_rsa`) are ignored via `.gitignore` and should not be committed.
