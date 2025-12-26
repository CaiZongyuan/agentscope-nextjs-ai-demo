# Vercel AI SDK Reasoning 事件兼容性修复指南

## 问题背景

在使用 AgentScope Runtime 作为后端、Vercel AI SDK 作为前端时，前端无法接收到 reasoning（推理）内容。

### 根本原因

后端发送的 reasoning 事件类型与 Vercel AI SDK 期望的不匹配：

| 后端发送（旧格式） | Vercel AI SDK 期望（新格式） |
|------------------|---------------------------|
| `response.reasoning_text.delta` | `response.reasoning_summary_text.delta` |
| `response.reasoning_text.done` | `response.reasoning_summary_part.done` |
| _(缺失)_ | `response.reasoning_summary_part.added` |

Vercel AI SDK 的 OpenAI Responses Provider 只能识别 `summary` 系列的事件类型。

## 解决方案分析

### 为什么 Language Model Middleware 不能解决？

Vercel AI SDK 的 Language Model Middleware 工作在 provider 解析 SSE 事件**之后**。由于 provider 无法识别 `response.reasoning_text.delta`，它根本不会产生 `reasoning-delta` 内部流事件，middleware 也就没有机会拦截。

```
数据流向:
后端 SSE → OpenAI Provider 解析 → 内部 Stream Parts → Middleware → UI
                    ↑
           问题发生在这里！
           未知事件被直接忽略
```

### 最终方案：修改后端适配器

直接修改 AgentScope Runtime 的 `response_api_adapter_utils.py`，使其发送正确的事件类型。

## 具体修改步骤

### 1. 修改 import 语句

移除旧的 import，添加新的：

```python
# 移除
from openai.types.responses import (
    ResponseReasoningTextDeltaEvent,
    ResponseReasoningTextDoneEvent,
)

# 添加
from openai.types.responses import (
    ResponseReasoningSummaryTextDeltaEvent,
    ResponseReasoningSummaryPartDoneEvent,
    ResponseReasoningSummaryPartAddedEvent,
)
```

### 2. 修改 `_handle_new_message` 方法

在 `MessageType.REASONING` 分支中添加 `response.reasoning_summary_part.added` 事件：

```python
elif message_event.type == MessageType.REASONING:
    # ... 原有代码 ...
    
    # 新增：发送 summary_part.added 事件
    summary_part_added_event = ResponseReasoningSummaryPartAddedEvent(
        type="response.reasoning_summary_part.added",
        item_id=message_event.id,
        output_index=self._output_index,
        part={"type": "summary_text", "text": ""},
        summary_index=0,
        sequence_number=0,
    )
    
    messages.append(item_added_event)
    messages.append(summary_part_added_event)  # 新增
```

### 3. 修改 `_create_reasoning_text_delta_event` 方法

```python
def _create_reasoning_text_delta_event(...):
    # 使用新的事件类型
    return ResponseReasoningSummaryTextDeltaEvent(
        type="response.reasoning_summary_text.delta",
        delta=text,
        item_id=content_event.msg_id,
        output_index=output_index,
        summary_index=0,  # 新增字段
        sequence_number=0,
    )
```

### 4. 修改 `_create_reasoning_text_done_event` 方法

```python
def _create_reasoning_text_done_event(...):
    # 使用新的事件类型
    return ResponseReasoningSummaryPartDoneEvent(
        type="response.reasoning_summary_part.done",
        item_id=content_event.msg_id,
        output_index=output_index,
        part={"type": "summary_text", "text": text},  # 新增字段
        summary_index=0,  # 新增字段
        sequence_number=0,
    )
```

## 应用修改

由于 AgentScope Runtime 是通过 pip 安装的包，需要将修改后的文件复制到包目录：

```bash
cp backend/docs/response_api_adapter_utils.py \
   backend/.venv/lib/python3.12/site-packages/agentscope_runtime/engine/deployers/adapter/responses/
```

然后重启后端服务。

> ⚠️ **注意**：每次执行 `uv sync` 或更新包时，这些修改会丢失，需要重新复制。

## 验证方法

1. 启动后端：`uv run python daemon_deploy.py`
2. 启动前端：`npm run dev` 或 `bun dev`
3. 发送一条会触发 reasoning 的消息（如复杂问题）
4. 检查前端是否正确显示 reasoning 内容

## 参考资料

- [OpenAI Responses API 事件类型](https://platform.openai.com/docs/api-reference/responses)
- [Vercel AI SDK Language Model Middleware](https://sdk.vercel.ai/docs/ai-sdk-core/middleware)
- [openai-responses-language-model.ts](https://github.com/vercel/ai/blob/main/packages/openai/src/responses/openai-responses-language-model.ts) - Vercel AI SDK 中处理 reasoning 事件的源码
