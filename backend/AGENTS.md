# Repository Guidelines

## Project Structure & Module Organization
- `agent_app.py` defines the AgentScope `AgentApp`, endpoints, and core agent wiring.
- `daemon_deploy.py` starts the app using a local deploy manager for development.
- `docs/` contains supporting notes (for example, `docs/example-completions.md`).
- `pyproject.toml` and `uv.lock` define Python dependencies.
- `.env.example` documents required environment variables; copy to `.env` for local runs.

## Build, Test, and Development Commands
- `uv sync`: install dependencies from `uv.lock` (preferred if `uv` is available).
- `uv run python daemon_deploy.py`: run the agent app locally in daemon mode.
- `python daemon_deploy.py`: run without `uv` if dependencies are already installed.
