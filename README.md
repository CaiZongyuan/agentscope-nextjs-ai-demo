# AgentScope NextJS AI Demo

**English | [中文](README-zh.md)**

A full-stack AI chat demo that connects a Next.js frontend with an AgentScope Runtime backend using OpenAI-compatible streaming APIs.

## Runtime Status

This project has been migrated to **AgentScope Runtime v1.1.0** (`backend/uv.lock`), and docs below follow the v1.1 architecture.

## What's Updated for Runtime v1.1.0

- `AgentApp` is used directly as the FastAPI app root in `backend/agent_app.py`.
- Resource lifecycle is managed through `lifespan`.
- Session/memory handling uses AgentScope native modules (`RedisSession`, `InMemoryMemory`).
- Query interruption handling follows `CancelledError` + `await agent.interrupt()`.
- Frontend calls Runtime OpenAI-compatible endpoint at:
  - `http://localhost:8090/compatible-mode/v1`

## Tech Stack

### Frontend
- Next.js 16
- React 19
- AI SDK 6 (`ai`, `@ai-sdk/react`, `@ai-sdk/openai`)
- TypeScript

### Backend
- Python 3.12+
- AgentScope Runtime 1.1.0
- AgentScope 1.0.16
- FastAPI / Uvicorn

## Quick Start

### 1. Install backend dependencies

```bash
cd backend
uv sync
# or
pip install -e .
```

### 2. Configure environment

```bash
cp backend/.env.example backend/.env
```

Set required keys in `backend/.env`:

```env
GLM_API_KEY=...
LINEAR_API_KEY=...
```

Optional keys:

```env
SILICONFLOW_API_KEY=...
MODELSCOPE_API_KEY=...
```

### 3. Start backend

```bash
cd backend
uv run python daemon_deploy.py
# or
uv run uvicorn agent_app:app --reload --port 8090
```

### 4. Start frontend

```bash
cd frontend
bun install
bun dev
```

### 5. Open app

- Frontend: `http://localhost:3000`
- Runtime API base: `http://localhost:8090/compatible-mode/v1`

## Project Structure

```text
agentscope-nextjs-ai-demo/
├── AGENTS.md
├── README.md
├── README-zh.md
├── frontend/
│   ├── app/page.tsx
│   ├── app/api/chat/route.ts
│   └── package.json
└── backend/
    ├── agent_app.py
    ├── daemon_deploy.py
    ├── pyproject.toml
    ├── uv.lock
    └── .env.example
```

## Data Flow

1. User sends a message from `frontend/app/page.tsx`.
2. Frontend route `frontend/app/api/chat/route.ts` calls AgentScope Runtime via OpenAI-compatible API.
3. Runtime executes the agent, tool calls, and streaming output.
4. Frontend renders response parts including `text` and `reasoning`.

## Useful Commands

### Frontend

```bash
cd frontend
bun dev
bun build
bun start
bun lint
```

### Backend

```bash
cd backend
uv run python daemon_deploy.py
uv run uvicorn agent_app:app --reload --port 8090
```

## Troubleshooting

- Backend fails at startup:
  - Check Python version (`>=3.12`).
  - Check `backend/.env` keys, especially `GLM_API_KEY` and `LINEAR_API_KEY`.
- Frontend cannot stream:
  - Confirm backend is running on `8090`.
  - Confirm `frontend/app/api/chat/route.ts` points to `http://localhost:8090/compatible-mode/v1`.
- Interruption behavior looks wrong:
  - Verify `CancelledError` handling and `await agent.interrupt()` are preserved in `backend/agent_app.py`.

## References

- AgentScope Runtime v1.1.0 Changelog:
  - https://runtime.agentscope.io/v1.1.0/en/CHANGELOG.html
- AgentScope Runtime Docs:
  - https://runtime.agentscope.io/
- AgentScope Docs:
  - https://agentscope.readthedocs.io/
