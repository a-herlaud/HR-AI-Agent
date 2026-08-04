from typing import Any, Optional

from fastapi import FastAPI
from langchain.agents import create_agent
from langchain_litellm import ChatLiteLLM
from langchain_mcp_adapters.client import MultiServerMCPClient
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from opentelemetry import trace
from langchain_core.messages import AIMessage


app = FastAPI()
langfuse = Langfuse()
tracer = trace.get_tracer(__name__)

client = MultiServerMCPClient(
    {
        "remote": {
            "transport": "streamable_http",
            "url": "http://mcp-server:8001/mcp",
        }
    }
)

llm = ChatLiteLLM(model="gemini/gemini-3.1-flash-lite")



def _extract_usage_details(messages) -> Optional[dict[str, int]]:
    totals = {"input": 0, "output": 0, "total": 0}
    found = False
    for m in messages:
        if not isinstance(m, AIMessage):
            continue
        um = _to_plain_dict(getattr(m, "usage_metadata", None))
        if not um:
            tu = (getattr(m, "response_metadata", {}) or {}).get("token_usage")
            um = _to_plain_dict(tu)
        if not um:
            continue
        found = True
        totals["input"] += um.get("input_tokens") or um.get("prompt_tokens") or 0
        totals["output"] += um.get("output_tokens") or um.get("completion_tokens") or 0
        totals["total"] += um.get("total_tokens") or 0
    return totals if found else None


@app.post("/prompt")
async def prompt_response(prompt: str):
    callback_handler = CallbackHandler()

    with tracer.start_as_current_span("prompt_response") as span:
        span.set_attribute("agent.prompt", prompt)

        with langfuse.start_as_current_observation(
            as_type="generation",
            name="prompt_response",
            input=prompt,
        ) as generation:
            tools = await client.get_tools()

            agent = create_agent(
                model=llm,
                tools=tools,
            )

            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": prompt}]},
                config={"callbacks": [callback_handler]},
            )

            response_message = response["messages"][-1]
            response_text = response_message.content
            usage_details = _extract_usage_details(response_message)

            span.set_attribute("agent.response", response_text)

            generation.update(output=response_text, usage_details=usage_details)

            return {
                "response": response_text,
                "usage_details": usage_details,
            }