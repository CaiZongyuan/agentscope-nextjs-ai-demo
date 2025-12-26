# Welcome to AgentScope Runtime Cookbook

## AgentScope Runtime V1.0 Release

AgentScope Runtime V1.0 builds upon the solid foundation of efficient agent deployment and secure sandbox execution, now offering **a unified “Agent as API” experience** across the full agent development lifecycle — from local development to production deployment — with expanded sandbox types, protocol compatibility, and a richer set of built‑in tools.

At the same time, the way agents integrate with runtime services has evolved from **black‑box module replacement** to a ***white‑box adapter pattern*** — enabling developers to preserve the native interfaces and behaviors of their existing agent frameworks, while embedding runtime capabilities such as state management, session history, and tool registration directly into the application lifecycle. This provides greater flexibility and seamless cross‑framework integration.

**Key improvements in V1.0:**

- **Unified dev/prod paradigm** — Consistent Agent Functional in both development and production environments.
- **Native multi-agent support** — Full compatibility with AgentScope’s multi-agent paradigms
- **Mainstream SDK & protocol integration** — OpenAI SDK support and Google A2A protocol compatibility
- **Visual Web UI** — Ready-to-use web chat interface immediately available after deployment
- **Expanded sandbox types** — GUI, Browser, FileSystem, Mobile, Cloud (most visualized via VNC)
- **Richer built-in tools** — Production-ready modules for Search, RAG, AIGC, Payment, and more
- **Flexible deployment modes** — Local threads/processes, Docker, Kubernetes, or hosted cloud

For more detailed change descriptions and the migration guide, please refer to: {doc}`CHANGELOG`

## What is AgentScope Runtime?

**AgentScope Runtime** is a full-stack agent runtime that tackles two core challenges: **efficient agent deployment** and **secure sandbox execution**. It ships with foundational services such as short- and long-term memory plus agent-state persistence, along with hardened sandbox infrastructure. Whether you need to orchestrate production-grade agents or guarantee safe tool interactions, AgentScope Runtime provides developer-friendly workflows with complete observability.

In V1.0, these services are exposed via an **adapter pattern**, enabling seamless integration with the native modules of different agent frameworks while preserving their native interfaces and behaviors, ensuring both compatibility and flexibility.

This cookbook walks you through building service-ready agent applications with **AgentScope Runtime**.

## Core Architecture

**⚙️ Agent Deployment Runtime (Engine)**

Provides `AgentApp` as the main entry point for agent applications, along with production‑grade infrastructure for deploying, managing, and training agents. It also includes built‑in services such as session history, long‑term memory, and agent state management.

**🔒 Sandbox Execution Runtime (Sandbox)**

Secure, isolated environments that let agents execute code, control browsers, manipulate files, and integrate MCP tools—without exposing your host system.

**🛠️ Production‑Grade Tool Services (Tool)**

Built on trusted third‑party API capabilities (such as Search, RAG, AIGC, Payment, etc.), these services are exposed through a unified SDK that provides standardized call interfaces, enabling agents to integrate and utilize these capabilities in a consistent way without worrying about differences or complexities in the underlying APIs.

**🔌 Adapter Pattern (Adapter)**

Adapts various runtime service modules (state management, session history, tool execution, etc.) to the native module interfaces of agent frameworks, allowing developers to directly invoke these capabilities while preserving native behaviors — enabling seamless integration and flexible extension.

## Why AgentScope Runtime?

* 🤖 **AS Native Runtime Framework** — Officially built and maintained by AgentScope, deeply integrated with its multi‑agent paradigms, adapter pattern, and tool usage to ensure optimal compatibility and performance.
* **🏗️ Deployment Infrastructure**: Built-in long memory, session, agent state, and sandbox control services
* **🔒 Sandbox Execution**: Isolated sandboxes keep browser, file, and MCP tooling safe
* ⚡ **Developer Friendly**: Simple deployment flows plus rich customization endpoints
* **📊 Observability**: End-to-end tracing and monitoring for runtime behavior

Start deploying agents and experimenting with the sandbox today!
