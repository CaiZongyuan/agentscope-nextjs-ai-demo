---
name: agentscope-sdk
description: This skill should be used when users need to work with AgentScope, a multi-agent platform for building AI-powered applications. It provides comprehensive guidance on agents, tools, memory management, models, RAG, workflows, evaluation, and development operations.
---

# AgentScope SDK

AgentScope is a flexible and easy-to-use multi-agent framework for building LLM-based applications with support for various AI providers. It enables creation of intelligent agents, tool integration, memory management, and multi-agent orchestration through a unified Python interface.

## Core Functionality

AgentScope provides a comprehensive platform for building AI-powered multi-agent applications. It supports agent creation with pre-built ReAct agents or custom agent classes, automatic tool schema generation, flexible memory management systems, and multi-provider model integration. The framework includes retrieval-augmented generation capabilities, sophisticated workflow orchestration patterns, evaluation frameworks, and development tools for monitoring and debugging.

## When to Use

This skill should be used when users need to work with AgentScope, a multi-agent platform for building AI-powered applications. It provides comprehensive guidance on agents, tools, memory management, models, RAG, workflows, evaluation, and development operations.

## Getting Started

Begin with the quickstart tutorials to understand core concepts:

- **Key Concepts**: Refer to `references/quickstart_key_concept.py` for foundational architecture including state management, message handling, tools, agents, and formatters
- **Message System**: Refer to `references/quickstart_message.py` for creating messages with multimodal content support, tool use handling, and serialization
- **Agent Basics**: Refer to `references/quickstart_agent.py` for ReAct agent features including realtime steering, parallel tool calls, and structured output

## Module Overview

### Agents Module
Create and customize agents using ReActAgent or build custom agents from AgentBase. Register agent skills for specialized capabilities.

- **Key APIs**: ReActAgent, AgentBase, UserAgent, PlanNotebook
- **Detailed documentation**: `references/task_agent.py`, `references/task_agent_skill.py`, `references/example_react_agent.py`

### Tools Module
Implement tool functions with automatic JSON schema generation, integrate MCP servers, and customize behavior using hooks.

- **Key APIs**: Toolkit, ToolResponse, HttpStatefulClient, StdIOStatefulClient, register_instance_hook
- **Detailed documentation**: `references/task_tool.py`, `references/task_hook.py`, `references/task_mcp.py`, `references/example_mcp.py`

### Memory Module
Manage conversation context with short-term and long-term memory systems, including compression strategies for token optimization.

- **Key APIs**: InMemoryMemory, MemoryBase, Mem0LongTermMemory, ReMePersonalLongTermMemory, MemoryWithCompress
- **Detailed documentation**: `references/task_memory.py`, `references/task_long_term_memory.py`, `references/example_memory_compress.py`

### Models Module
Integrate multiple LLM providers including OpenAI, DashScope, Anthropic, Gemini, and Ollama with unified interfaces for chat, embeddings, and text-to-speech.

- **Key APIs**: DashScopeChatModel, OpenAIChatModel, AnthropicChatModel, GeminiChatModel, DashScopeTextEmbedding, DashScopeRealtimeTTSModel, OpenAITokenCounter
- **Detailed documentation**: `references/task_model.py`, `references/task_embedding.py`, `references/task_token.py`, `references/task_tts.py`

### RAG Module
Build retrieval-augmented generation systems with document readers, vector embeddings, and knowledge base storage.

- **Key APIs**: TextReader, PDFReader, ImageReader, SimpleKnowledge, QdrantStore, DashScopeTextEmbedding, retrieve_knowledge
- **Detailed documentation**: `references/task_rag.py`, `references/example_rag_basic.py`

### Planning Module
Enable agents to break down complex tasks into subtasks with manual or agent-managed plan specification and execution tracking.

- **Key APIs**: PlanNotebook, Plan, SubTask
- **Detailed documentation**: `references/task_plan.py`, `references/example_plan_agent.py`, `references/example_plan_manual.py`

### State Management Module
Manage agent states with automatic variable registration and session-level persistence.

- **Key APIs**: StateModule, register_state, JSONSession, state_dict, load_state_dict
- **Detailed documentation**: `references/task_state.py`, `references/task_prompt.py`, `references/task_tracing.py`

### Pipelines Module
Orchestrate multi-agent workflows with sequential and fanout execution patterns using message broadcasting.

- **Key APIs**: MsgHub, sequential_pipeline, fanout_pipeline, SequentialPipeline, FanoutPipeline
- **Detailed documentation**: `references/task_pipeline.py`

### Workflows Module
Implement common multi-agent patterns including concurrent execution, conversations, handoffs, debates, and routing.

- **Key APIs**: ReActAgent, MsgHub, RoutingChoice, ToolResponse
- **Detailed documentation**: `references/workflow_concurrent_agents.py`, `references/workflow_conversation.py`, `references/workflow_handoffs.py`, `references/workflow_multiagent_debate.py`, `references/workflow_routing.py`

### Evaluation Module
Assess agent performance with custom metrics, benchmarks, and evaluators supporting sequential and parallel execution.

- **Key APIs**: BenchmarkBase, MetricBase, GeneralEvaluator, RayEvaluator, ToyBenchmark, CheckEqual
- **Detailed documentation**: `references/task_eval.py`

### Studio Module
Monitor and debug agent applications with AgentScope Studio's web interface for visualization and tracing.

- **Key APIs**: agentscope.init, as_studio
- **Detailed documentation**: `references/task_studio.py`

### Browser Automation Module
Automate web browsing tasks using Playwright MCP integration with specialized BrowserAgent capabilities.

- **Key APIs**: BrowserAgent, StdIOStatefulClient, ReActAgent
- **Detailed documentation**: `references/example_browser_agent.py`, `references/example_browser_agent_impl.py`

## Key APIs

**Agent Creation**
- `ReActAgent`: Pre-built reasoning and acting agent with tool support
- `AgentBase`: Base class for custom agent implementation
- `UserAgent`: Specialized agent for user interactions

**Message Management**
- `Msg`: Message objects with multimodal content support
- `MsgHub`: Broadcast messages to multiple agents
- `TextBlock`, `ToolUseBlock`, `ToolResultBlock`: Content block types

**Tool Integration**
- `Toolkit`: Manage tool functions with automatic schema generation
- `register_tool_function`: Register Python functions as tools
- `register_mcp_client`: Integrate MCP servers for external tools

**Memory Systems**
- `InMemoryMemory`: Short-term conversation memory
- `Mem0LongTermMemory`: Persistent memory using mem0
- `MemoryWithCompress`: Automatic memory compression

**Model Integration**
- `DashScopeChatModel`: Alibaba DashScope LLM integration
- `OpenAIChatModel`: OpenAI API integration
- `DashScopeTextEmbedding`: Text embedding generation
- `OpenAITokenCounter`: Token counting for API usage estimation

**Workflow Orchestration**
- `sequential_pipeline`: Execute agents in sequence
- `fanout_pipeline`: Execute agents in parallel
- `PlanNotebook`: Task planning and subtask management

**State Management**
- `StateModule`: Base class for stateful agents
- `JSONSession`: Session persistence with JSON storage
- `register_state`: Decorator for automatic state registration

## Common Patterns

**Agent Initialization Pattern**
```python
agent = ReActAgent(
    name="assistant",
    model_config=DashScopeChatModel(),
    memory=InMemoryMemory(),
    tools=[...]
)
```

**Message Exchange Pattern**
```python
msg = Msg(name="user", content="Hello world")
response = await agent(msg)
```

**Tool Registration Pattern**
```python
toolkit = Toolkit()
toolkit.register_tool_function(execute_python_code)
agent = ReActAgent(tools=toolkit.get_json_schemas())
```

**Pipeline Execution Pattern**
```python
async with MsgHub("hub") as hub:
    await sequential_pipeline([agent1, agent2], hub)
```

**State Management Pattern**
```python
class MyStatefulAgent(StateModule):
    def __init__(self):
        super().__init__()
        self.register_state("counter", 0)
```

**MCP Integration Pattern**
```python
client = HttpStatefulClient("http://localhost:8000/sse")
toolkit.register_mcp_client(client)
```

## Workflow

1. **Initialize AgentScope** with model configuration and API keys
2. **Create agents** using ReActAgent or custom AgentBase subclasses
3. **Register tools** via Toolkit or integrate MCP servers for external capabilities
4. **Configure memory** with InMemoryMemory for short-term or long-term memory classes
5. **Orchestrate workflows** using pipelines, MsgHub, or custom coordination logic
6. **Monitor execution** through AgentScope Studio for debugging and visualization

Refer to detailed documentation in `references/` directory for specific implementation patterns and advanced configurations.

## Resource References

**Quick Start**
- `references/quickstart_agent.py` - Agent basics with ReActAgent
- `references/quickstart_key_concept.py` - Core architecture concepts
- `references/quickstart_message.py` - Message system overview

**Agent Development**
- `references/task_agent.py` - Agent initialization and planning
- `references/task_agent_skill.py` - Agent skill registration
- `references/example_react_agent.py` - Custom agent examples

**Tool Integration**
- `references/task_tool.py` - Tool function implementation
- `references/task_mcp.py` - MCP server integration
- `references/task_hook.py` - Lifecycle hooks for customization

**Memory Management**
- `references/task_memory.py` - Short-term memory usage
- `references/task_long_term_memory.py` - Persistent memory systems
- `references/example_memory_compress.py` - Memory compression strategies

**Model Integration**
- `references/task_model.py` - Multi-provider LLM integration
- `references/task_embedding.py` - Text and multimodal embeddings
- `references/task_token.py` - Token counting for cost estimation
- `references/task_tts.py` - Text-to-speech capabilities

**RAG Implementation**
- `references/task_rag.py` - Comprehensive RAG guide
- `references/example_rag_basic.py` - Basic RAG example

**Workflow Patterns**
- `references/workflow_conversation.py` - User-agent and multi-agent conversations
- `references/workflow_routing.py` - Query routing to specialized agents
- `references/workflow_handoffs.py` - Orchestrator-worker delegation
- `references/workflow_concurrent_agents.py` - Parallel agent execution
- `references/workflow_multiagent_debate.py` - Consensus through debate

**State Management**
- `references/task_state.py` - State module usage
- `references/task_prompt.py` - Message formatting for LLM providers
- `references/task_tracing.py` - OpenTelemetry tracing setup

**Evaluation and Monitoring**
- `references/task_eval.py` - Agent evaluation framework
- `references/task_studio.py` - Studio deployment and usage

**Advanced Examples**
- `references/example_browser_agent.py` - Browser automation with Playwright
- `references/example_plan_agent.py` - Planning with ReActAgent
- `references/example_plan_manual.py` - Manual plan specification
