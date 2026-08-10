from collections.abc import Sequence
from typing import Any, Optional

from fastapi import FastAPI
from langchain.agents import create_agent
from langchain_litellm import ChatLiteLLM
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from opentelemetry import trace
from langchain_core.messages import AIMessage
from agent_workflow import graph


app = FastAPI()
langfuse = Langfuse()
tracer = trace.get_tracer(__name__)

@app.post("/prompt")
async def prompt_response(prompt: str) -> dict[str, Any]:
    callback_handler = CallbackHandler()

    with tracer.start_as_current_span("prompt_response") as span:
        span.set_attribute("agent.prompt", prompt)

        result = await graph.ainvoke(
            {
                "user_request": prompt,
            },
            config={
                "callbacks": [callback_handler],
            },
        )

        response_message = result.get("final_report", "")
        span.set_attribute("agent.response", response_message)

    return {
        "response": response_message,
        "graph_state": result,
    }