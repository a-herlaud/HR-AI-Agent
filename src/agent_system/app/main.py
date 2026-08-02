from fastapi import FastAPI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_litellm import ChatLiteLLM
from langchain.agents import create_agent
import asyncio

app = FastAPI()

client = MultiServerMCPClient(
    {
        "remote": {
            "transport": "streamable_http",
            "url": "http://mcp-server:8001/mcp",
        }
    }
)


llm = ChatLiteLLM(
    model="gemini/gemini-3.1-flash-lite", 
    )




@app.get("/prompt")
async def prompt_response():
    tools = await client.get_tools()

    # Pick a tool
    tool = next(t for t in tools if t.name == "get_quarter_kpis")

    # Invoke it directly
    result = await tool.ainvoke({})

    print(result)

    agent = create_agent(
        model=llm,
        tools=tools,
    )

    response = await agent.ainvoke(   # <-- was agent.invoke(...)
        {
            "messages": [
                {"role": "user", "content": "What the HR KPIs for this quarter ?"}
            ]
        }
    )

    return response["messages"][-1].content













