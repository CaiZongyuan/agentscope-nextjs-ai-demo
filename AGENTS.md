# Repository Guidelines

## Project Structure & Module Organization
- `frontend/`: Next.js 16 + AI SDK 6 chat UI.
- `frontend/app/page.tsx`: chat UI and reasoning rendering.
- `frontend/app/api/chat/route.ts`: server route that proxies to AgentScope Runtime OpenAI-compatible API.
- `backend/agent_app.py`: AgentScope Runtime app (`AgentApp`) and all endpoints.
- `backend/daemon_deploy.py`: local daemon deploy entrypoint.
- `backend/pyproject.toml`, `backend/uv.lock`: Python dependencies (includes `agentscope-runtime==1.1.0` in lockfile).

## Build, Test, and Development Commands
- Frontend install: `cd frontend && bun install` (or `npm install`).
- Frontend dev: `cd frontend && bun dev`.
- Frontend lint: `cd frontend && bun lint`.
- Backend install: `cd backend && uv sync` (or `pip install -e .`).
- Backend run (daemon): `cd backend && uv run python daemon_deploy.py`.
- Backend run (uvicorn): `cd backend && uv run uvicorn agent_app:app --reload --port 8090`.

## AgentScope Runtime v1.1 Conventions
- Keep `AgentApp` as the FastAPI app root; add custom routes directly with FastAPI decorators.
- Manage startup/shutdown resources via `lifespan`.
- Use AgentScope native memory/session modules (`InMemoryMemory`, `RedisSession`, etc.) inside query handlers.
- On interruption, catch `asyncio.CancelledError` and call `await agent.interrupt()` before re-raising.
- Prefer OpenAI-compatible endpoint usage through `http://localhost:8090/compatible-mode/v1`.

## Coding Style & Naming Conventions
- Python: PEP 8, type-friendly async code, keep endpoint logic small and explicit.
- TypeScript: strict mode, use small React components, keep API route logic server-only.
- Keep comments minimal and only for non-obvious logic.

## Testing Guidelines
- Frontend baseline check: `cd frontend && bun lint`.
- Backend smoke check: start backend and validate `/compatible-mode/v1/chat/completions` can stream.
- If behavior touches interruption/session logic, manually verify stop + resume flow.

## Commit & PR Guidelines
- Keep commits focused (docs/runtime/frontend changes separated when possible).
- In PR description, include updated runtime version assumptions and env var changes.
- When changing API paths or startup commands, update `AGENTS.md` and `README*.md` together.

## Environment & Secrets
- Backend `.env` keys used by current app:
  - `GLM_API_KEY` (default model provider)
  - `LINEAR_API_KEY` (required by MCP Linear client)
  - `SILICONFLOW_API_KEY`, `MODELSCOPE_API_KEY` (optional alternative providers)
- Never hardcode keys or tokens in source files.

## Documentation Rules
- Keep `AGENTS.md` and `README.md` consistent after architecture or dependency changes.
- If runtime behavior changes, update endpoint paths, env vars, and startup commands in both docs in the same PR.
