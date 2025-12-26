# Implementation Plan: OpenAI-Compatible Chat Completions Endpoint

## Overview
Add a `/v1/chat/completions` endpoint to the AgentScope Runtime backend that:
- Accepts OpenAI-formatted chat completion requests
- Streams responses in OpenAI SSE format with `data: {...}\n\n`
- Extracts `reasoning_content` from AgentScope REASONING message type
- Filters reasoning based on `enable_thinking` parameter

## User Requirements (Clarified)
- **Endpoint**: `/v1/chat/completions` (standard OpenAI path)
- **Reasoning**: Separate `reasoning_content` field in delta chunks
- **Streaming**: Streaming only (no non-streaming support)
- **enable_thinking**: When false, exclude reasoning_content from response

---

## Files to Create

### 1. `adapters/chat_completions/__init__.py`
Empty init file for the chat completions adapter package.

### 2. `adapters/chat_completions/chat_completions_protocol_adapter.py`
Main protocol adapter following the `ResponseAPIDefaultAdapter` pattern.

**Key classes:**
- `ChatCompletionsProtocolAdapter` - Extends `ProtocolAdapter`
- `SSE_HEADERS` - SSE response headers

**Key methods:**
- `_handle_requests()` - Main request handler with timeout control
- `_generate_stream_response()` - SSE streaming generator
- `add_endpoint()` - Register `/v1/chat/completions` endpoint

### 3. `adapters/chat_completions/chat_completions_adapter_utils.py`
Conversion utilities for request/response transformation.

**Key classes:**
- `ChatCompletionsExecutor` - Executes agent and yields chat completion chunks

**Key methods:**
- `execute()` - Main execution loop, converts events to chunks
- `_convert_chat_request_to_agent_request()` - OpenAI format → AgentRequest
- `_convert_event_to_chunks()` - Route events to appropriate converters
- `_convert_reasoning_to_chunks()` - REASONING messages → reasoning_content chunks
- `_convert_message_to_content_chunks()` - MESSAGE → content chunks
- `_create_final_chunk()` - Final chunk with finish_reason and usage

---

## Implementation Steps

### Step 1: Create Adapter Structure
Create the `adapters/chat_completions/` directory with `__init__.py`, `chat_completions_protocol_adapter.py`, and `chat_completions_adapter_utils.py`.

### Step 2: Implement ChatCompletionsExecutor
Following the `ResponseAPIExecutor` pattern:
- Accept OpenAI chat completion request
- Convert to AgentRequest
- Execute agent query function
- Convert AgentScope events to ChatCompletionChunk objects
- Filter reasoning based on `enable_thinking` parameter

### Step 3: Implement Request Conversion
Map OpenAI format to AgentRequest:
```python
{
  "model": "glm-4.7",
  "messages": [{"role": "user", "content": "hello"}],
  "stream": true,
  "enable_thinking": true
}
```
↓
```python
AgentRequest(
  input=[Message(role="user", type="message", content=[TextContent(text="hello")])],
  model="glm-4.7",
  stream=True
)
```

### Step 4: Implement Event-to-Chunk Conversion
Process AgentScope event types:
- **BaseResponse** → Metadata chunks
- **Message (type=MESSAGE)** → `content` in delta
- **Message (type=REASONING)** → `reasoning_content` in delta (if enable_thinking=True)
- **Content** → Delta chunks for streaming

### Step 5: Implement SSE Streaming
Generate SSE format:
```
data: {...}\n\n
data: {...}\n\n
data: [DONE]\n\n
```

### Step 6: Register Protocol Adapter in agent_app.py
Import and register the `ChatCompletionsProtocolAdapter` with the AgentApp.

---

## Critical Reference Files

1. **`.venv/.../response_api_protocol_adapter.py`**
   - Reference implementation for protocol adapter pattern, SSE streaming, error handling

2. **`.venv/.../response_api_adapter_utils.py`**
   - Reference for `ResponsesAdapter` with bidirectional conversion logic (lines 1953-2003 for REASONING handling)

3. **`.venv/.../oai_llm.py`**
   - Contains `create_chat_completion_chunk()` function and `OpenAIMessage` type

4. **`.venv/.../agent_schemas.py`**
   - Defines `MessageType`, `ContentType`, `Message`, `Content`, `Event` types

5. **`agent_app.py`**
   - Current AgentApp configuration, will register the new adapter

---

## Expected Output Format

**Request:**
```json
{
  "model": "glm-4.7",
  "messages": [{"role": "user", "content": "hello"}],
  "stream": true,
  "enable_thinking": true
}
```

**Response (SSE chunks):**
```
data: {
  "id": "uuid",
  "object": "chat.completion.chunk",
  "created": 1764042665,
  "model": "glm-4.7",
  "choices": [{
    "index": 0,
    "delta": {
      "role": "assistant",
      "reasoning_content": "好的"
    },
    "logprobs": null,
    "finish_reason": null
  }]
}

data: {
  "choices": [{
    "delta": {"content": "纱", "reasoning_content": null},
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 6,
    "completion_tokens": 1552,
    "total_tokens": 1558
  }
}
data: [DONE]
```

---

## Key Implementation Patterns

### Reasoning Extraction Pattern
```python
def _convert_reasoning_to_chunks(self, message: Message, request_id: str):
    reasoning_text = ""
    if message.content:
        for content_item in message.content:
            if content_item.type == ContentType.TEXT:
                reasoning_text = content_item.text
                break

    # Stream character by character
    for char in reasoning_text:
        yield create_chat_completion_chunk(
            message=OpenAIMessage(reasoning_content=char),
            model_name="agent",
            id=request_id
        )
```

### enable_thinking Filter
```python
if event.type == MessageType.REASONING:
    if not enable_thinking:
        return []  # Skip reasoning
    return self._convert_reasoning_to_chunks(event, request_id)
```

### SSE Format
```python
async def _generate_stream_response(self, request, request_id):
    async for chunk in self._executor.execute(request):
        chunk_data = chunk.model_dump(exclude_none=True)
        data = json.dumps(chunk_data, ensure_ascii=False)
        yield f"data: {data}\n\n"

    yield "data: [DONE]\n\n"
```

# Examples

## input:

post -> https://api.siliconflow.cn/v1/chat/completions

body:
```json
{
  "model": "glm-4.7",
  "messages": [
    {
      "role": "user",
      "content": "hello"
    }
  ],
  "stream":true,
  "enable_thinking": true
}
```

## output:

sse:
```json
data: {
    "id": "0e9642e9-9af6-4eb1-9c13-8c90d6b13ef3",
    "object": "chat.completion.chunk",
    "created": 1764042665,
    "model": "deepseek-reasoner",
    "system_fingerprint": "fp_ffc7281d48_prod0820_fp8_kvcache",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": null,
                "reasoning_content": ""
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}

data: {
    "id": "0e9642e9-9af6-4eb1-9c13-8c90d6b13ef3",
    "object": "chat.completion.chunk",
    "created": 1764042665,
    "model": "deepseek-reasoner",
    "system_fingerprint": "fp_ffc7281d48_prod0820_fp8_kvcache",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": null,
                "reasoning_content": "好的"
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}


data: {
    "id": "0e9642e9-9af6-4eb1-9c13-8c90d6b13ef3",
    "object": "chat.completion.chunk",
    "created": 1764042665,
    "model": "deepseek-reasoner",
    "system_fingerprint": "fp_ffc7281d48_prod0820_fp8_kvcache",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": null,
                "reasoning_content": "，"
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}

中间省略 reasoning_content。

data: {
    "id": "0e9642e9-9af6-4eb1-9c13-8c90d6b13ef3",
    "object": "chat.completion.chunk",
    "created": 1764042665,
    "model": "deepseek-reasoner",
    "system_fingerprint": "fp_ffc7281d48_prod0820_fp8_kvcache",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": "纱",
                "reasoning_content": null
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}

data: {
    "id": "0e9642e9-9af6-4eb1-9c13-8c90d6b13ef3",
    "object": "chat.completion.chunk",
    "created": 1764042665,
    "model": "deepseek-reasoner",
    "system_fingerprint": "fp_ffc7281d48_prod0820_fp8_kvcache",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": "！",
                "reasoning_content": null
            },
            "logprobs": null,
            "finish_reason": null
        }
    ]
}

中间省略正常的 content （非reasoning_content部分）

data: {
    "id": "0e9642e9-9af6-4eb1-9c13-8c90d6b13ef3",
    "object": "chat.completion.chunk",
    "created": 1764042665,
    "model": "deepseek-reasoner",
    "system_fingerprint": "fp_ffc7281d48_prod0820_fp8_kvcache",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": "",
                "reasoning_content": null
            },
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 6,
        "completion_tokens": 1552,
        "total_tokens": 1558,
        "prompt_tokens_details": {
            "cached_tokens": 0
        },
        "completion_tokens_details": {
            "reasoning_tokens": 199
        },
        "prompt_cache_hit_tokens": 0,
        "prompt_cache_miss_tokens": 6
    }
}

data: [DONE
]
```