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