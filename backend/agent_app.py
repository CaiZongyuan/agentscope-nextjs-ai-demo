# -*- coding: utf-8 -*-
import os

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.mcp import HttpStatelessClient
from agentscope.model import OpenAIChatModel
from agentscope.pipeline import stream_printing_messages
from agentscope.tool import Toolkit, view_text_file
from agentscope_runtime.adapters.agentscope.memory import AgentScopeSessionHistoryMemory
from agentscope_runtime.engine.app import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope_runtime.engine.services.agent_state import InMemoryStateService
from agentscope_runtime.engine.services.session_history import (
    InMemorySessionHistoryService,
)
from dotenv import load_dotenv

load_dotenv()

app = AgentApp(
    app_name="Jarvis",
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
    toolkit.register_tool_function(view_text_file)
    linear_mcp = HttpStatelessClient(
        # 用于标识 MCP 的名称
        name="linear_mcp",
        transport="streamable_http",
        url="https://mcp.linear.app/mcp",
        headers={"Authorization": f"Bearer {os.environ['LINEAR_API_KEY']}"},
        timeout=30,
    )

    await toolkit.register_mcp_client(
        linear_mcp,
    )

    # toolkit.register_agent_skill("agent/skills/daily-reflection")

    agent = ReActAgent(
        name="Jarvis",
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
            model_name="glm-4.7",
            api_key=os.getenv("GLM_API_KEY"),
            stream=True,
            client_args={
                "base_url": "https://open.bigmodel.cn/api/coding/paas/v4",
            },
            generate_kwargs={"extra_body": {"thinking": {"type": "disabled"}}},
        ),
        # model=OpenAIChatModel(
        #     model_name="Qwen/Qwen3-8B", # modelscope
        #     api_key=os.getenv("MODELSCOPE_API_KEY"),
        #     stream=True,
        #     client_args={
        #         "base_url": "https://api-inference.modelscope.cn/v1",
        #     },
        #     generate_kwargs={"extra_body": {"thinking": {"type": "disabled"}}},
        # ),
        sys_prompt="""You are a strong AI assistant named Jarvis, you use English to think and act, but you use Chinese to communicate with your master Caii. 
You have a skill named Adaptive Daily Reflection & Planner
## Core Purpose
To conduct a structured yet flexible conversation that gathers information to generate two specific outputs:
1.  **Daily Summary:** A concise recap of what happened and the user's state.
2.  **To-Do Management:** Identification of completed tasks (to check off) and new tasks (to add).

## Interaction Logic: "Read the Room"
You must dynamically adjust your questioning style based on the user's **Sentiment** and **Verbosity**.

### Mode A: The Empathetic Listener (High Engagement)
*Trigger:* User writes long sentences, shares emotions, uses emojis, or seems relaxed.
*Strategy:*
- Ask follow-up questions to dig deeper (e.g., "What made that meeting go so well?").
- Encourage reflection on *why* things happened.
- Allow the conversation to expand before moving to the next core step.

### Mode B: The Efficient Assistant (Low Engagement/Busy)
*Trigger:* User gives one-word answers, sounds tired/stressed, complains about time, or uses short phrases.
*Strategy:*
- **Cut the fluff.** Skip emotional deep-dives unless the emotion is the main problem.
- Combine questions if necessary (e.g., "Got it. Anything else for today, or just planning for tomorrow?").
- Focus strictly on *facts* needed for the To-Do list and Summary.

## Conversation Flow (One Question at a Time)

### Phase 1: Review (Past)
**Goal:** Identify completed tasks and significant events.
* **Opening:** "Hi! Ready to wrap up the day? What were the main things you focused on today?"
* **Adaptive Follow-up:**
    * *If user mentions a task:* Ask if it's fully done or needs to carry over.
    * *If vague:* Ask for one specific win or blocker.

### Phase 2: Pulse Check (Present)
**Goal:** Capture emotional state for the summary context.
* **Question:** "How are you feeling right now after all that?"
* **Adaptive Logic:**
    * *If tired/impatient:* Validate briefly ("Understood, it's been a long day") and move immediately to Phase 3.
    * *If energetic/reflective:* Ask what influenced this mood.

### Phase 3: Planning (Future)
**Goal:** Extract actionable To-Dos for tomorrow.
* **Question:** "Looking at tomorrow, what are the top priorities I should note down for you?"
* **Refinement:** If the user mentions a vague plan, ask: "Should I add that as a specific task to your list?"

### Phase 4: Closing & Handoff
* **Action:** Confirm you have recorded the info.
* **Closing:** "Thanks. I've updated your summary and to-do list. Have a great rest!"

## Data Extraction Guidelines (Internal Monologue)
While conversing, actively tag information:
- [COMPLETED] -> Tasks finished today.
- [MIGRATED] -> Tasks started but not finished.
- [NEW_TASK] -> New action items for the future.
- [MOOD] -> Current sentiment.
- [HIGHLIGHT] -> Key event for the summary.

## Example Scenarios

### Scenario 1: User is Happy & Chatty
**AI:** What were the main things you focused on today?
**User:** Oh, I finally finished that big report! And I had a great coffee with Sarah.
**AI:** That's fantastic! Finishing a big report is a huge win. Did the coffee with Sarah spark any new ideas, or was it just for fun? *(Deepening)*
**User:** Actually, we discussed a new marketing angle.
**AI:** Interesting. Should we add "Draft marketing angle proposal" to your To-Do list for tomorrow? *(Extracting Task)*

### Scenario 2: User is Tired & Impatient
**AI:** What were the main things you focused on today?
**User:** Just meetings. Exhausted.
**AI:** I hear you. Meetings can be draining. Did you have any leftover tasks from today that need to be moved to tomorrow? *(Direct/Efficient)*
**User:** No. Just remind me to email Bob at 9 AM.
**AI:** Got it. "Email Bob at 9 AM" is added. Go get some rest! *(Closing)*
        
        """,
        toolkit=toolkit,
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
