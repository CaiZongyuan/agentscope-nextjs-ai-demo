import {
  streamText,
  UIMessage,
  convertToModelMessages,
  tool,
  stepCountIs,
} from "ai";
import { createOpenAI } from "@ai-sdk/openai";
import { z } from "zod";

const customOpenAI = createOpenAI({
  baseURL: "http://localhost:8090/compatible-mode/v1",
  apiKey: process.env.CUSTOM_OPENAI_API_KEY || "EMPTY",
});

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: customOpenAI("agent-model"), // Use a generic or placeholder model name
    messages: convertToModelMessages(messages),
    stopWhen: stepCountIs(5),
    tools: {
      weather: tool({
        description: "Get the weather in a location (fahrenheit)",
        inputSchema: z.object({
          location: z.string().describe("The location to get the weather for"),
        }),
        execute: async ({ location }) => {
          const temperature = Math.round(Math.random() * (90 - 32) + 32);
          return {
            location,
            temperature,
          };
        },
      }),
    },
  });

  return result.toUIMessageStreamResponse({});
}
