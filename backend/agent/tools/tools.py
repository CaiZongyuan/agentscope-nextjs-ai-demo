import asyncio

from agentscope_runtime.tools import Tool
from pydantic import BaseModel, Field


class WeatherInput(BaseModel):
    city: str = Field(..., description="City to check")
    unit: str = Field(default="celsius", description="Temperature unit")


class WeatherOutput(BaseModel):
    summary: str
    temperature: float


class WeatherTool(Tool[WeatherInput, WeatherOutput]):
    name = "weather_lookup"
    description = "Fetches the current weather for a city"

    async def _arun(self, args: WeatherInput, **kwargs) -> WeatherOutput:
        # Replace with real API logic
        return WeatherOutput(summary=f"Sunny in {args.city}", temperature=26.5)


async def main():
    tool = WeatherTool()
    result = await tool.arun(WeatherInput(city="Hangzhou"))
    print(result.summary)
    print(tool.function_schema)  # ready for tool registration


asyncio.run(main())
