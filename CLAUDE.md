# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack AI chat application demonstrating AgentScope integration with a Next.js frontend. The application features real-time streaming chat with AI agents that support reasoning display and tool execution.

## Architecture

### Frontend (`/frontend/`)
- **Next.js 16** with App Router and React 19
- **Vercel AI SDK** for streaming chat functionality (`@ai-sdk/react`, `@ai-sdk/openai`)
- **Tailwind CSS v4** for styling
- **TypeScript** for type safety

### Backend (`/backend/`)
- **AgentScope Runtime** for agent orchestration
- **ReActAgent** implementation with memory management
- **Streaming API** with OpenAI-compatible endpoints
- **Async Python** with AgentApp framework

## Development Commands

### Frontend Development
```bash
cd frontend
# Install dependencies
bun install  # or npm install

# Run development server
bun dev  # or npm run dev

# Build for production
bun build  # or npm run build

# Start production server
bun start  # or npm start

# Lint code
bun lint  # or npm run lint
```

### Backend Development
```bash
cd backend
# Install dependencies (requires Python 3.12+)
pip install -e .
# or using uv
uv sync

# Run development server
uvicorn agent_app:app --reload --port 8090

# Or use daemon deployment
python daemon_deploy.py
```

## Environment Setup

Copy `.env.example` to `.env` in the backend directory:
```bash
GLM_API_KEY=your_glm_api_key
SILICONFLOW_API_KEY=your_siliconflow_api_key
```

## Key Architecture Patterns

### AgentScope Integration
- **agent_app.py**: Main AgentApp with streaming query handlers
- **ReActAgent**: Reasoning and acting agent with memory
- **State Service**: In-memory agent persistence
- **Session Service**: Conversation history management

### Frontend Chat Implementation
- **app/page.tsx**: Main chat interface with reasoning display
- **app/chat/route.ts**: API route handling streaming responses
- **useChat**: Vercel AI SDK hook for chat state management
- **Tool Calls**: Visual display of agent tool executions

### API Architecture
- **OpenAI-compatible**: `/chat/completions` endpoint
- **Streaming**: Server-sent events for real-time responses
- **Custom Routes**: Weather tools and agent interactions

## Development Notes

### Vercel AI SDK v6 Documentation
**IMPORTANT**: Claude has limited familiarity with Vercel AI SDK v6. When working with AI SDK features, always reference the official documentation in:
- `frontend/docs/AI-SDK-Core/` - Core SDK documentation (text generation, structured data, providers, middleware, etc.)
- `frontend/docs/AI-SDK-UI/` - UI hooks and components documentation (useChat, streaming, message protocols, etc.)

Before implementing AI SDK features, read the relevant documentation files to ensure correct usage of the latest v6 APIs and patterns.

### Frontend Development
- Uses App Router (pages directory not supported)
- Tailwind CSS v4 with PostCSS configuration
- React 19 features with concurrent rendering
- TypeScript strict mode enabled

### Backend Development
- AgentScope runtime manages agent lifecycle
- Async/await patterns throughout
- Stateful agents with session persistence
- Tool integration for extended capabilities

### LLM Integration
- Currently configured for GLM-4.6 model
- OpenAI-compatible API interface
- Support for multiple providers (GLM, SiliconFlow)
- Streaming responses for real-time chat

## File Structure Highlights

- `frontend/app/page.tsx`: Chat UI with reasoning display
- `frontend/app/chat/route.ts`: Backend API integration
- `backend/agent_app.py`: Main agent application
- `backend/daemon_deploy.py`: Local deployment manager
- `backend/.env.example`: Environment variables template

## Running the Full Application

1. Start backend: `cd backend && python daemon_deploy.py`
2. Start frontend: `cd frontend && bun dev`
3. Access at `http://localhost:3000`

The frontend connects to the backend at `http://localhost:8090` by default.