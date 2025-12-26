---
name: agentscope-runtime
description: This skill should be used when users need to work with AgentScope Runtime for deploying, managing, and operating AI agent applications. It provides comprehensive guidance on AgentApp deployment, service architecture (State, Memory, Session, Sandbox), API integration, CLI workflows, deployment strategies, tools and skills management, and advanced features including real-time processing and training environments.
---

# AgentScope Runtime

AgentScope Runtime is a full-stack agent framework designed for efficient deployment and secure execution of AI agents. It provides a unified "Agent as API" experience with built-in sandbox execution, multi-agent orchestration, and comprehensive observability features.

## Core Architecture

AgentScope Runtime consists of four core components:

- **Agent**: The fundamental unit that processes inputs and generates outputs using LLMs and tools
- **AgentApp**: Service wrapper that transforms agents into HTTP APIs with streaming support
- **Runner**: Execution engine that manages agent lifecycle and query processing
- **Deployer**: Infrastructure abstraction for deploying across local, cloud, and serverless environments

The framework uses an adapter pattern for services, enabling flexible backend implementations for state management, memory storage, session history, and sandbox execution. Built-in support for OpenAI-compatible APIs, Google A2A protocol, and MCP tools ensures seamless integration with existing ecosystems.

## When to Use

Use AgentScope Runtime when:
- Deploying AI agents as production services with HTTP APIs
- Building multi-agent systems with service discovery via A2A registry
- Requiring secure, isolated tool execution in sandboxed environments
- Managing agent state, memory, and conversation sessions across deployments
- Implementing streaming responses with Server-Sent Events (SSE)
- Orchestrating complex workflows with ReAct agents and tool chains
- Running agents at scale on Kubernetes, serverless platforms, or local infrastructure

## Module Overview

### Getting Started
**Functionality**: Introduces AgentScope Runtime V1.0 with quickstart guides for building and deploying the first agent application. Covers installation, configuration, and basic deployment workflows.
**Key Topics**: Installation, project setup, ReActAgent creation, AgentApp deployment, streaming responses
**Detailed documentation**: `references/intro.md`, `references/quickstart.md`, `references/README.md`, `references/concept.md`

### Core Architecture
**Functionality**: Explains the modular architecture including engine components, protocol specifications, and service patterns. Provides the foundation for understanding runtime internals.
**Key Topics**: Engine modules (App, Runner, Deployers, Services), JSON protocol for agent communication, message structures, streaming capabilities, protocol adapters
**Detailed documentation**: `references/engine.md`, `references/protocol.md`, `references/service.md`

### AgentApp & API Integration
**Functionality**: Comprehensive guide to AgentApp framework for deploying agents as HTTP services with streaming, lifecycle hooks, health checks, and custom endpoints.
**Key Topics**: AgentApp initialization, `app.run()`, `app.query()`, SSE streaming, OpenAI-compatible endpoints, lifecycle hooks, custom endpoints, CLI commands, WebUI integration
**Detailed documentation**: `references/agent_app.md`, `references/call.md`, `references/cli.md`, `references/webui.md`, `references/use.md`

### Services
**Functionality**: Covers the four core services for agent orchestration: State Service for persistent state management, Memory Service for long-term memory, Session History Service for conversation tracking, and Sandbox Service for isolated tool execution.
**Key Topics**: Service adapters, backend implementations (InMemory, Redis, Tablestore), lifecycle management, service factory pattern, environment management
**Detailed documentation**: `references/service.md`, `references/state.md`, `references/memory.md`, `references/session_history.md`, `references/sandbox.md`, `references/environment_manager.md`

### Deployment Strategies
**Functionality**: Provides five deployment methods ranging from local development to production-grade serverless deployments, with detailed configuration examples.
**Key Topics**: Local daemon deployment, detached processes, Kubernetes deployment, ModelStudio serverless, AgentRun serverless, Docker containerization, GPU support
**Detailed documentation**: `references/deployment.md`, `references/advanced_deployment.md`

### Tutorials
**Functionality**: Step-by-step tutorials for building practical agent applications with ReAct patterns, browser automation, and tool integration.
**Key Topics**: ReAct agent implementation, browser sandbox tools, Python code execution, multi-turn conversations, OpenAI-compatible mode
**Detailed documentation**: `references/react_agent.md`

### Tools & Skills
**Functionality**: Explains tool integration modes, skill import workflows, external adapters, and directory management for extending agent capabilities.
**Key Topics**: Ready-to-use tools, sandboxed tools, skill adapters (JSONSchema, OpenAPI, OpenAI, LangChain), remote skill loading, internal skill categories (tool, llm, knowledge, workflow)
**Detailed documentation**: `references/tool.md`, `references/tools.md`, `references/index.md`, `references/alipay.md`

### Advanced Sandbox
**Functionality**: Advanced sandbox configurations including remote deployment, custom environments, and training sandboxes for agent evaluation with public datasets.
**Key Topics**: Remote sandbox servers, custom sandbox classes, Docker image building, AppWorld training, BFCL evaluation, troubleshooting
**Detailed documentation**: `references/advanced.md`, `references/training_sandbox.md`, `references/troubleshooting.md`

### Integrations
**Functionality**: Integration guides for A2A service registry, ModelStudio components (RAG, Search, Image Generation), and real-time audio processing.
**Key Topics**: A2A registry with Nacos, RAG components, intelligent search, text-to-image generation, ASR/TTS clients, real-time audio streaming
**Detailed documentation**: `references/a2a_registry.md`, `references/modelstudio_rag.md`, `references/modelstudio_search.md`, `references/modelstudio_generations.md`, `references/realtime_clients.md`

### Observability
**Functionality**: Tracing, monitoring, and testing capabilities for production deployments with event tracking and error handling.
**Key Topics**: Tracer decorators, context managers, log handlers, event tracking, test samples (unit, sandbox, deployment, integrated)
**Detailed documentation**: `references/tracing.md`, `references/ut.md`

## Workflow

### Build and Deploy Your First Agent

1. **Install dependencies**:
   ```bash
   pip install agentscope-runtime
   ```

2. **Create a ReAct agent with tools**:
   ```python
   from agentscope.agents import ReActAgent
   from agentscope.models import DashScopeChatModel
   from agentscope.tools import execute_python_code

   model = DashScopeChatModel()

   agent = ReActAgent(
       name="assistant",
       model_config=model,
       tools=[execute_python_code],
   )
   ```

3. **Wrap in AgentApp**:
   ```python
   from agentscope_runtime import AgentApp
   from agentscope_runtime.services import InMemoryStateService, InMemorySessionHistoryService

   app = AgentApp(
       agent=agent,
       state_service=InMemoryStateService(),
       session_history_service=InMemorySessionHistoryService(),
   )
   ```

4. **Deploy the service**:
   ```python
   app.run(host="localhost", port=8090)
   ```

5. **Query the agent**:
   ```python
   response = app.query("Calculate fibonacci(10)")
   ```

For detailed step-by-step tutorials, refer to `references/quickstart.md` and `references/react_agent.md`.

### Using Services for State and Memory

Services in AgentScope Runtime use adapters to provide flexible backend implementations:

1. **State Service** - Persist agent state across turns and sessions:
   ```python
   from agentscope_runtime.services import RedisStateService

   state_service = RedisStateService(redis_url="redis://localhost:6379")

   # Save state
   await state_service.save_state(agent_id="agent_1", state=agent.state_dict())

   # Load state
   state = await state_service.export_state(agent_id="agent_1")
   ```

2. **Memory Service** - Store long-term memories across sessions:
   ```python
   from agentscope_runtime.services import TablestoreMemoryService

   memory_service = TablestoreMemoryService(
       endpoint="https://tablestore.aliyuncs.com"
   )

   # Add memory
   await memory_service.add(
       agent_id="agent_1",
       user_id="user_1",
       memory="User prefers Python over JavaScript"
   )
   ```

3. **Session History Service** - Track conversation sessions:
   ```python
   from agentscope_runtime.services import RedisSessionHistoryService

   session_service = RedisSessionHistoryService(redis_url="redis://localhost:6379")

   # Get conversation history
   history = await session_service.get_session(
       agent_id="agent_1",
       user_id="user_1",
       session_id="session_123"
   )
   ```

Refer to `references/service.md`, `references/state.md`, `references/memory.md`, and `references/session_history.md` for comprehensive service documentation.

### Sandbox Tool Execution

Execute tools in isolated environments for security:

1. **Use sandbox tools**:
   ```python
   from agentscope_runtime.tools import browser_navigate, browser_take_screenshot
   from agentscope_runtime.services import SandboxService

   sandbox_service = SandboxService()

   agent = ReActAgent(
       name="web_agent",
       model_config=model,
       tools=[browser_navigate, browser_take_screenshot],
       sandbox_service=sandbox_service,
   )
   ```

2. **Connect to sandbox environments**:
   ```python
   from agentscope_runtime import EnvironmentManager

   env_manager = EnvironmentManager()
   sandbox = await env_manager.connect(
       user_id="user_1",
       tool_name="browser_navigate"
   )
   ```

For advanced sandbox configuration and custom environments, see `references/sandbox.md`, `references/advanced.md`, and `references/environment_manager.md`.

### CLI Workflows

AgentScope Runtime provides a comprehensive CLI for agent management:

```bash
# Start an interactive chat session
agentscope chat --config agent_config.yaml

# Deploy an agent service
agentscope deploy --mode local --config agent_config.yaml

# Launch Web UI
agentscope web --config agent_config.yaml

# Manage sandbox deployments
agentscope sandbox list
agentscope sandbox stop <sandbox_id>
```

Refer to `references/cli.md` for complete CLI documentation and common workflows.

## Common Usage Patterns

### Pattern 1: Streaming Responses with SSE

Enable real-time streaming for agent responses:

```python
from agentscope_runtime import AgentApp

app = AgentApp(agent=agent)

@app.endpoint("/stream")
async def stream_query(query: str):
    async for chunk in app.stream_query(query):
        yield chunk
```

The `/process` endpoint provides built-in SSE streaming. See `references/call.md` for API details.

### Pattern 2: Multi-Turn Conversations

Maintain conversation context across multiple interactions:

```python
response1 = await app.query(
    query="My name is Alice",
    user_id="user_1",
    session_id="chat_123"
)

response2 = await app.query(
    query="What's my name?",
    user_id="user_1",
    session_id="chat_123"  # Same session maintains context
)
```

SessionHistoryService automatically tracks conversation history. Refer to `references/session_history.md`.

### Pattern 3: OpenAI-Compatible Integration

Use AgentScope Runtime with OpenAI SDK clients:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8090/compatible-mode/v1",
    api_key="dummy"
)

response = client.chat.completions.create(
    model="agent",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

The `/compatible-mode/v1/responses` endpoint provides OpenAI compatibility. See `references/call.md`.

### Pattern 4: Multi-Agent with A2A Registry

Enable service discovery for multi-agent systems:

```python
from agentscope_runtime import AgentApp
from agentscope_runtime.integrations import A2ARegistry, NacosRegistry

registry = NacosRegistry(server_addresses="localhost:8848")

app = AgentApp(
    agent=agent,
    a2a_config={
        "registry": registry,
        "name": "math_agent",
        "host": "localhost",
        "port": 8090
    }
)
```

Agents can discover and communicate with each other through the registry. See `references/a2a_registry.md`.

## Resource References

### Getting Started
- Introduction and overview: `references/intro.md`
- Quickstart tutorial: `references/quickstart.md`
- Core concepts: `references/concept.md`
- Detached process deployment: `references/README.md`

### AgentApp & API
- AgentApp framework: `references/agent_app.md`
- API invocation (streaming, OpenAI-compatible): `references/call.md`
- CLI commands: `references/cli.md`
- WebUI integration: `references/webui.md`
- Async usage patterns: `references/use.md`

### Core Architecture
- Engine modules: `references/engine.md`
- Protocol specification: `references/protocol.md`
- Service architecture: `references/service.md`

### Services
- State Service: `references/state.md`
- Memory Service: `references/memory.md`
- Session History Service: `references/session_history.md`
- Sandbox Service: `references/sandbox.md`
- Environment Manager: `references/environment_manager.md`

### Deployment
- Basic deployment: `references/deployment.md`
- Advanced deployment methods: `references/advanced_deployment.md`
- More Deploy Examples: `references/deployments-examples/`
    - agentrun_deploy: `references/deployments-examples/agentrun_deploy/`
    - daemon_local_deploy: `references/deployments-examples/daemon_local_deploy/`
    - detached_local_deploy: `references/deployments-examples/detached_local_deploy/`

### Tools & Skills
- Tool overview: `references/tool.md`
- External tools catalog: `references/tools.md`
- Skill import and adapters: `references/index.md`
- Alipay skill example: `references/alipay.md`

### Advanced Features
- Advanced sandbox configuration: `references/advanced.md`
- Training sandbox (AppWorld, BFCL): `references/training_sandbox.md`
- Troubleshooting: `references/troubleshooting.md`

### Integrations
- A2A Registry: `references/a2a_registry.md`
- ModelStudio RAG: `references/modelstudio_rag.md`
- ModelStudio Search: `references/modelstudio_search.md`
- ModelStudio Image Generation: `references/modelstudio_generations.md`
- Real-time audio (ASR/TTS): `references/realtime_clients.md`

### Observability
- Tracing and monitoring: `references/tracing.md`
- Test samples reference: `references/ut.md`

### Tutorials
- ReAct Agent tutorial: `references/react_agent.md`
