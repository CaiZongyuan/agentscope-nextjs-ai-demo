import { streamText, UIMessage, convertToModelMessages } from "ai";
import { createOpenAI } from "@ai-sdk/openai";
// import { createOpenAICompatible } from "@ai-sdk/openai-compatible";

// const glm = createOpenAICompatible({
//   name: "glm",
//   apiKey: process.env.GLM_API_KEY,
//   baseURL: "https://open.bigmodel.cn/api/coding/paas/v4",
// });

const agentScopeRuntime = createOpenAI({
  baseURL: "http://localhost:8090/compatible-mode/v1",
  apiKey: process.env.CUSTOM_OPENAI_API_KEY || "EMPTY",
});

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: agentScopeRuntime("agent-model"),
    // model: glm.chatModel("glm-4.7"),
    messages: await convertToModelMessages(messages),
    onChunk: ({ chunk }) => {
      // 使用 onChunk 回调进行调试，不会消费流
      console.log("Chunk:", chunk);
    },
  });

  return result.toUIMessageStreamResponse({});
}
