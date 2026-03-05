# AgentScope NextJS AI 演示

一个使用 OpenAI 兼容流式接口，将 Next.js 前端与 AgentScope Runtime 后端连接起来的全栈 AI 聊天示例。

## 运行时版本

本项目已迁移到 **AgentScope Runtime v1.1.0**（见 `backend/uv.lock`），本文档已按 v1.1 架构更新。

## v1.1.0 关键更新

- 在 `backend/agent_app.py` 中直接使用 `AgentApp` 作为 FastAPI 应用根。
- 使用 `lifespan` 管理启动与关闭资源。
- 使用 AgentScope 原生会话/记忆模块（`RedisSession`、`InMemoryMemory`）。
- 中断处理采用 `CancelledError` + `await agent.interrupt()`。
- 前端调用 Runtime 的 OpenAI 兼容地址：
  - `http://localhost:8090/compatible-mode/v1`

## 技术栈

### 前端
- Next.js 16
- React 19
- AI SDK 6（`ai`、`@ai-sdk/react`、`@ai-sdk/openai`）
- TypeScript

### 后端
- Python 3.12+
- AgentScope Runtime 1.1.0
- AgentScope 1.0.16
- FastAPI / Uvicorn

## 快速开始

### 1. 安装后端依赖

```bash
cd backend
uv sync
# 或
pip install -e .
```

### 2. 配置环境变量

```bash
cp backend/.env.example backend/.env
```

在 `backend/.env` 中设置必填项：

```env
GLM_API_KEY=...
LINEAR_API_KEY=...
```

可选项：

```env
SILICONFLOW_API_KEY=...
MODELSCOPE_API_KEY=...
```

### 3. 启动后端

```bash
cd backend
uv run python daemon_deploy.py
# 或
uv run uvicorn agent_app:app --reload --port 8090
```

### 4. 启动前端

```bash
cd frontend
bun install
bun dev
```

### 5. 访问

- 前端：`http://localhost:3000`
- Runtime API 基础地址：`http://localhost:8090/compatible-mode/v1`

## 项目结构

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

## 数据流

1. 用户在 `frontend/app/page.tsx` 发送消息。
2. 前端路由 `frontend/app/api/chat/route.ts` 通过 OpenAI 兼容接口调用 AgentScope Runtime。
3. Runtime 执行智能体、工具调用并输出流式结果。
4. 前端渲染 `text` 与 `reasoning` 等消息片段。

## 常用命令

### 前端

```bash
cd frontend
bun dev
bun build
bun start
bun lint
```

### 后端

```bash
cd backend
uv run python daemon_deploy.py
uv run uvicorn agent_app:app --reload --port 8090
```

## 故障排查

- 后端启动失败：
  - 检查 Python 版本（`>=3.12`）。
  - 检查 `backend/.env`，尤其是 `GLM_API_KEY` 和 `LINEAR_API_KEY`。
- 前端无法流式返回：
  - 确认后端运行在 `8090`。
  - 确认 `frontend/app/api/chat/route.ts` 指向 `http://localhost:8090/compatible-mode/v1`。
- 中断行为异常：
  - 检查 `backend/agent_app.py` 中 `CancelledError` 和 `await agent.interrupt()` 逻辑是否保留。

## 参考

- AgentScope Runtime v1.1.0 变更日志：
  - https://runtime.agentscope.io/v1.1.0/en/CHANGELOG.html
- AgentScope Runtime 文档：
  - https://runtime.agentscope.io/
- AgentScope 文档：
  - https://agentscope.readthedocs.io/
