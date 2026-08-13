from collections.abc import Awaitable, Callable
from typing import Any, TypedDict
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_litellm import ChatLiteLLM
import asyncio
import json
from langchain.agents import create_agent

llm = ChatLiteLLM(model="gemini/gemini-3.1-flash-lite")


async def load_tools() -> dict[str, Any]:
    client = MultiServerMCPClient(
        {
            "remote": {
                "transport": "streamable_http",
                "url": "http://mcp-server:8001/mcp",
            }
        }
    )

    tools = await client.get_tools()

    tool_map = {tool.name: tool for tool in tools}

    return tool_map

class AgentState(TypedDict, total=False):
    user_request: str
    route: list[str]
    hr_analysis: str
    research: str
    final_report: str


from langgraph.prebuilt import create_react_agent
# or, if you're on langgraph v1+: from langchain.agents import create_agent as create_react_agent

def create_my_agent(
    system_prompt: str,
    output_key: str,
    tools: list[Any] | None = None,
) -> Callable[[AgentState], Awaitable[dict[str, str]]]:
    tools = tools or []
    react_agent = create_react_agent(llm, tools, prompt=system_prompt)

    async def agent(state: AgentState) -> dict[str, str]:
        content = state["user_request"]

        if output_key == "final_report":
            context_parts = []
            hr_analysis = state.get("hr_analysis")
            research = state.get("research")

            if hr_analysis:
                context_parts.append(f"HR analysis:\n{hr_analysis}")
            if research:
                context_parts.append(f"Research:\n{research}")

            if context_parts:
                content += "\n\n" + "\n\n".join(context_parts)

        result = await react_agent.ainvoke({"messages": [HumanMessage(content=content)]})
        return {output_key: result["messages"][-1].content}

    return agent

def create_coordinator() -> Callable[[AgentState], dict[str, list[str]]]:
    planner = llm.with_structured_output(
        {
            "title": "RoutingDecision",
            "type": "object",
            "properties": {
                "route": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "hr_agent",
                            "web_researcher",
                        ],
                    },
                },
            },
            "required": ["route"],
        }
    )

    def coordinator(state: AgentState) -> dict[str, list[str]]:
        result = planner.invoke(
            [
                SystemMessage(
                    content="""
You are a workflow coordinator.

Choose which agents should execute.

Possible agents:
- hr_agent
- web_researcher

Return only the list of agents.
"""
                ),
                HumanMessage(content=state["user_request"]),
            ]
        )

        return {
            "route": result["route"]
        }

    return coordinator

tool_map = asyncio.run(load_tools())

coordinator = create_coordinator()

hr_agent = create_my_agent(
    """
    You are an HR specialist. Specialist to gather quarter or monthly KPIs
    Return the result from the tool you use or the string Nothing if you didn't call any tool
    """,
    "hr_analysis",
    [tool_map["get_kpis"] ,tool_map["get_quarter_kpis"], tool_map["get_monthly_kpis"], tool_map["get_employees_kpis"]],
)

web_researcher = create_my_agent(
    """
    You are a web researcher specialized in finding up-to-date information.

    Workflow:
    1. ALWAYS call web_research first to find relevant articles.
    2. After receiving URLs from web_research, ALWAYS call fetch_url for each relevant URL.
    3. Only write the final JSON response after fetch_url has returned the article contents.

    Do not summarize directly from search results. Use fetch_url content as the source for summaries.

    Return JSON:
    [
    {
        "url": "...",
        "description": "Maximum 200 words summarizing the article."
    }
    ]
    """,
    "research",
    [tool_map["web_search"], tool_map["fetch_url"], tool_map["get_today_date"]],
)

reporter = create_my_agent(
    """
Combine every available result into one final report.

If only one specialist ran, use only that output.
If multiple specialists ran, merge them.
Keep your response bellow 200 words
""",
    "final_report",
)