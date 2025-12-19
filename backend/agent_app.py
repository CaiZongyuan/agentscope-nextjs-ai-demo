# -*- coding: utf-8 -*-
import os

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.model import OpenAIChatModel
from agentscope.pipeline import stream_printing_messages
from agentscope.tool import Toolkit, execute_python_code

from agentscope_runtime.adapters.agentscope.memory import (
    AgentScopeSessionHistoryMemory,
)
from agentscope_runtime.engine.app import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope_runtime.engine.services.agent_state import (
    InMemoryStateService,
)
from agentscope_runtime.engine.services.session_history import (
    InMemorySessionHistoryService,
)

from dotenv import load_dotenv

load_dotenv()

app = AgentApp(
    app_name="Friday",
    app_description="A helpful assistant",
)


@app.init
async def init_func(self):
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()

    await self.state_service.start()
    await self.session_service.start()


@app.shutdown
async def shutdown_func(self):
    await self.state_service.stop()
    await self.session_service.stop()


@app.query(framework="agentscope")
async def query_func(
    self,
    msgs,
    request: AgentRequest = None,
    **kwargs,
):
    assert kwargs is not None, "kwargs is Required for query_func"
    session_id = request.session_id
    user_id = request.user_id

    state = await self.state_service.export_state(
        session_id=session_id,
        user_id=user_id,
    )

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="Friday",
        ## siliconflow
        # model=OpenAIChatModel(
        #     model_name="Qwen/Qwen3-8B",
        #     api_key=os.getenv("SILICONFLOW_API_KEY"),
        #     stream=True,
        #     client_args={
        #         "base_url": "https://api.siliconflow.cn/v1",
        #     },
        #     generate_kwargs={"extra_body": {"enable_thinking": False}},
        # ),
        model=OpenAIChatModel(
            model_name="glm-4.6",
            api_key=os.getenv("GLM_API_KEY"),
            stream=True,
            client_args={
                "base_url": "https://open.bigmodel.cn/api/coding/paas/v4",
            },
            generate_kwargs={"extra_body": {"thinking": {"type": "disabled"}}},
        ),
        sys_prompt="You're a helpful assistant named Friday.",
        # toolkit=toolkit,
        memory=AgentScopeSessionHistoryMemory(
            service=self.session_service,
            session_id=session_id,
            user_id=user_id,
        ),
        formatter=OpenAIChatFormatter(),
    )

    if state:
        agent.load_state_dict(state)

    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(msgs),
    ):
        yield msg, last

    state = agent.state_dict()

    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=state,
    )


# 2. Create multiple endpoints for AgentApp
@app.endpoint("/sync")
def sync_handler(request: AgentRequest):
    return {"status": "ok", "payload": request}


@app.endpoint("/async")
async def async_handler(request: AgentRequest):
    return {"status": "ok", "payload": request}


@app.endpoint("/stream_async")
async def stream_async_handler(request: AgentRequest):
    for i in range(5):
        yield f"async chunk {i}, with request payload {request}\n"


@app.endpoint("/stream_sync")
def stream_sync_handler(request: AgentRequest):
    for i in range(5):
        yield f"sync chunk {i}, with request payload {request}\n"


@app.task("/task", queue="celery1")
def task_handler(request: AgentRequest):
    import time

    time.sleep(30)
    return {"status": "ok", "payload": request}


@app.task("/atask")
async def atask_handler(request: AgentRequest):
    import asyncio

    await asyncio.sleep(15)
    return {"status": "ok", "payload": request}


print("✅ AgentApp configuration completed")
