# AgentScope NextJS AI Demo

**English | [中文](README-zh.md)**

A full-stack AI chat application demonstrating integration between AgentScope (Python) and Next.js (React), featuring real-time streaming conversations with reasoning display and tool execution capabilities.

## 🚀 Features

- **Real-time Streaming Chat** - Instant responses with server-sent events
- **Reasoning Display** - See the AI agent's thought process in real-time
- **Tool Integration** - Extended capabilities through agent tools (weather, etc.)
- **Session Persistence** - Conversation history and continuity
- **Multi-LLM Support** - Compatible with OpenAI, GLM, and other providers
- **Modern Stack** - Next.js 16, React 19, TypeScript, Tailwind CSS v4

## 📋 Prerequisites

- **Node.js** 18+ (with [bun](https://bun.sh/) or npm)
- **Python** 3.12+
- **API keys** for LLM providers (see Environment Setup)

## 🛠 Tech Stack

### Frontend
- **Next.js 16** - React framework with App Router
- **React 19** - UI library with concurrent features
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Utility-first CSS framework
- **Vercel AI SDK** - Streaming AI chat functionality

### Backend
- **Python 3.12+** - Runtime environment
- **AgentScope Runtime** - Agent orchestration framework
- **AgentScope** - Agent implementation toolkit
- **AsyncIO** - Asynchronous programming
- **FastAPI/Uvicorn** - API server

### AI Integration
- **GLM-4.6** (智谱AI) - Primary configured model
- **OpenAI API** - Compatible interface
- **SiliconFlow** - Alternative provider

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd agentscope-nextjs-ai-demo
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
# OR using uv (faster)
uv sync
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
bun install
# OR using npm
npm install
```

### 4. Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
cp backend/.env.example backend/.env
```

Add your API keys to `backend/.env`:
```env
GLM_API_KEY=your_glm_api_key_here
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

### 5. Run the Application

**Option 1: Start both services**

```bash
# Terminal 1 - Start backend
cd backend
python daemon_deploy.py

# Terminal 2 - Start frontend
cd frontend
bun dev
```

**Option 2: Start backend with uvicorn**

```bash
cd backend
uvicorn agent_app:app --reload --port 8090
```

### 6. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8090

## 📁 Project Structure

```
agentscope-nextjs-ai-demo/
├── frontend/                 # Next.js frontend application
│   ├── app/
│   │   ├── page.tsx         # Main chat interface
│   │   └── chat/
│   │       └── route.ts     # API route for backend integration
│   ├── package.json         # Frontend dependencies
│   └── ...                  # Next.js config files
├── backend/                  # Python AgentScope backend
│   ├── agent_app.py         # Main agent application
│   ├── daemon_deploy.py     # Local deployment manager
│   ├── pyproject.toml       # Python project configuration
│   ├── .env.example         # Environment variables template
│   └── ...                  # AgentScope runtime files
└── README.md                # This file
```

## 🔧 Development

### Frontend Development Commands
```bash
cd frontend
bun dev          # Start development server
bun build        # Build for production
bun start        # Start production server
bun lint         # Run ESLint
```

### Backend Development Commands
```bash
cd backend
python daemon_deploy.py     # Run with daemon
uvicorn agent_app:app --reload --port 8090  # Run with uvicorn
```

### Environment Variables

Required variables in `backend/.env`:
- `GLM_API_KEY` - API key for GLM model
- `SILICONFLOW_API_KEY` - API key for SiliconFlow provider

## 🏗 Architecture

### Frontend Architecture
- **App Router** - Modern Next.js routing
- **AI SDK Integration** - Streaming chat with `@ai-sdk/react`
- **Component-based** - Modular React components
- **TypeScript** - Full type safety

### Backend Architecture
- **AgentApp** - Main application container
- **ReActAgent** - Reasoning and acting agent
- **Streaming API** - OpenAI-compatible endpoints
- **State Management** - Session persistence and memory

### Data Flow
1. User sends message via frontend
2. Frontend calls `/chat/completions` API
3. Backend processes with AgentScope agent
4. Agent reasons and uses tools if needed
5. Streaming response sent back to frontend
6. Frontend displays reasoning and final response

## 🤖 AI Agent Features

### Reasoning Display
- See agent's thought process in real-time
- Transparency in decision-making
- Step-by-step problem solving

### Tool Integration
- Weather information retrieval
- Extensible tool system
- Custom tool development support

### Session Management
- Conversation history tracking
- Context preservation
- State export/import capabilities

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version (requires 3.12+)
- Verify API keys in `.env` file
- Install dependencies: `pip install -e .`

**Frontend connection errors:**
- Ensure backend is running on port 8090
- Check CORS configuration
- Verify API route in `app/chat/route.ts`

**API key errors:**
- Verify keys in `backend/.env`
- Check API provider status
- Ensure proper key format

### Debug Mode

Enable detailed logging:
```bash
# Backend
export AGENTSCOPE_LOG_LEVEL=DEBUG
python daemon_deploy.py

# Frontend - Next.js will show detailed errors in development
```

## 📚 Learn More

- **[AgentScope Documentation](https://agentscope.readthedocs.io/)**
- **[Next.js Documentation](https://nextjs.org/docs)**
- **[Vercel AI SDK](https://sdk.vercel.ai/)**
- **[React 19 Features](https://react.dev/blog/2024/04/25/react-19)**
- **[Tailwind CSS v4](https://tailwindcss.com/blog/tailwindcss-v4-alpha)**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AgentScope Team** - For the excellent agent framework
- **Vercel** - For the AI SDK and Next.js
- **OpenAI** - For the API specification
- **GLM (智谱AI)** - For providing the model API