# AgentScope NextJS AI 演示

一个展示 AgentScope (Python) 与 Next.js (React) 集成的全栈 AI 聊天应用程序，具有实时流式对话、推理过程展示和工具执行能力。

## 🚀 功能特性

- **实时流式聊天** - 通过服务器发送事件实现即时响应
- **推理过程展示** - 实时查看 AI 代理的思维过程
- **工具集成** - 通过代理工具扩展能力（天气查询等）
- **会话持久化** - 对话历史和连续性
- **多 LLM 支持** - 兼容 OpenAI、GLM 和其他提供商
- **现代技术栈** - Next.js 16、React 19、TypeScript、Tailwind CSS v4

## 📋 环境要求

- **Node.js** 18+（推荐使用 [bun](https://bun.sh/) 或 npm）
- **Python** 3.12+
- **LLM 提供商的 API 密钥**（参见环境设置）

## 🛠 技术栈

### 前端
- **Next.js 16** - 使用 App Router 的 React 框架
- **React 19** - 具有并发特性的 UI 库
- **TypeScript** - 类型安全
- **Tailwind CSS v4** - 实用优先的 CSS 框架
- **Vercel AI SDK** - 流式 AI 聊天功能

### 后端
- **Python 3.12+** - 运行环境
- **AgentScope Runtime** - 代理编排框架
- **AgentScope** - 代理实现工具包
- **AsyncIO** - 异步编程
- **FastAPI/Uvicorn** - API 服务器

### AI 集成
- **GLM-4.6** (智谱AI) - 主要配置模型
- **OpenAI API** - 兼容接口
- **SiliconFlow** - 备选提供商

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone <repository-url>
cd agentscope-nextjs-ai-demo
```

### 2. 后端设置

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -e .
# 或使用 uv（更快）
uv sync
```

### 3. 前端设置

```bash
cd frontend

# 安装依赖
bun install
# 或使用 npm
npm install
```

### 4. 环境配置

在 `backend/` 目录中创建 `.env` 文件：

```bash
cp backend/.env.example backend/.env
```

将您的 API 密钥添加到 `backend/.env`：
```env
GLM_API_KEY=your_glm_api_key_here
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

### 5. 运行应用程序

**选项 1：启动两个服务**

```bash
# 终端 1 - 启动后端
cd backend
python daemon_deploy.py

# 终端 2 - 启动前端
cd frontend
bun dev
```

**选项 2：使用 uvicorn 启动后端**

```bash
cd backend
uvicorn agent_app:app --reload --port 8090
```

### 6. 访问应用程序

在浏览器中打开：
- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8090

## 📁 项目结构

```
agentscope-nextjs-ai-demo/
├── frontend/                 # Next.js 前端应用程序
│   ├── app/
│   │   ├── page.tsx         # 主聊天界面
│   │   └── chat/
│   │       └── route.ts     # 后端集成的 API 路由
│   ├── package.json         # 前端依赖
│   └── ...                  # Next.js 配置文件
├── backend/                  # Python AgentScope 后端
│   ├── agent_app.py         # 主代理应用程序
│   ├── daemon_deploy.py     # 本地部署管理器
│   ├── pyproject.toml       # Python 项目配置
│   ├── .env.example         # 环境变量模板
│   └── ...                  # AgentScope 运行时文件
└── README.md                # 英文文档
└── README-zh.md             # 中文文档（本文件）
```

## 🔧 开发

### 前端开发命令
```bash
cd frontend
bun dev          # 启动开发服务器
bun build        # 生产构建
bun start        # 启动生产服务器
bun lint         # 运行 ESLint
```

### 后端开发命令
```bash
cd backend
python daemon_deploy.py     # 使用守护进程运行
uvicorn agent_app:app --reload --port 8090  # 使用 uvicorn 运行
```

### 环境变量

在 `backend/.env` 中需要的变量：
- `GLM_API_KEY` - GLM 模型的 API 密钥
- `SILICONFLOW_API_KEY` - SiliconFlow 提供商的 API 密钥

## 🏗 架构

### 前端架构
- **App Router** - 现代 Next.js 路由
- **AI SDK 集成** - 使用 `@ai-sdk/react` 的流式聊天
- **组件化** - 模块化 React 组件
- **TypeScript** - 完全类型安全

### 后端架构
- **AgentApp** - 主应用程序容器
- **ReActAgent** - 推理和行动代理
- **流式 API** - OpenAI 兼容端点
- **状态管理** - 会话持久化和内存

### 数据流
1. 用户通过前端发送消息
2. 前端调用 `/chat/completions` API
3. 后端使用 AgentScope 代理处理
4. 代理推理并在需要时使用工具
5. 流式响应发送回前端
6. 前端显示推理过程和最终响应

## 🤖 AI 代理功能

### 推理过程展示
- 实时查看代理的思维过程
- 决策制定的透明度
- 循序渐进的问题解决

### 工具集成
- 天气信息检索
- 可扩展的工具系统
- 自定义工具开发支持

### 会话管理
- 对话历史跟踪
- 上下文保持
- 状态导出/导入功能

## 🐛 故障排除

### 常见问题

**后端无法启动：**
- 检查 Python 版本（需要 3.12+）
- 验证 `.env` 文件中的 API 密钥
- 安装依赖：`pip install -e .`

**前端连接错误：**
- 确保后端在端口 8090 上运行
- 检查 CORS 配置
- 验证 `app/chat/route.ts` 中的 API 路由

**API 密钥错误：**
- 验证 `backend/.env` 中的密钥
- 检查 API 提供商状态
- 确保密钥格式正确

### 调试模式

启用详细日志：
```bash
# 后端
export AGENTSCOPE_LOG_LEVEL=DEBUG
python daemon_deploy.py

# 前端 - Next.js 将在开发中显示详细错误
```

## 📚 了解更多

- **[AgentScope 文档](https://agentscope.readthedocs.io/)**
- **[Next.js 文档](https://nextjs.org/docs)**
- **[Vercel AI SDK](https://sdk.vercel.ai/)**
- **[React 19 特性](https://react.dev/blog/2024/04/25/react-19)**
- **[Tailwind CSS v4](https://tailwindcss.com/blog/tailwindcss-v4-alpha)**

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature-name`
3. 提交更改：`git commit -am 'Add feature'`
4. 推送到分支：`git push origin feature-name`
5. 提交拉取请求

## 📄 许可证

本项目基于 MIT 许可证授权 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- **AgentScope 团队** - 提供优秀的代理框架
- **Vercel** - 提供 AI SDK 和 Next.js
- **OpenAI** - 提供 API 规范
- **GLM (智谱AI)** - 提供模型 API