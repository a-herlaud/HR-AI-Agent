from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from agents import AgentState, coordinator, hr_agent, web_researcher, reporter

builder = StateGraph(AgentState)

builder.add_node("coordinator", coordinator)
builder.add_node("hr_agent", hr_agent)
builder.add_node("web_researcher", web_researcher)
builder.add_node("reporter", reporter)


builder.add_edge(START, "coordinator")


def router(state: AgentState):
    sends = [Send(agent_name, state) for agent_name in state["route"]]

    # If nothing to execute, go directly to the reporter.
    if not sends:
        sends.append(Send("reporter", state))

    return sends


builder.add_conditional_edges(
    "coordinator",
    router,
)


builder.add_edge("hr_agent", "reporter")
builder.add_edge("web_researcher", "reporter")

builder.add_edge("reporter", END)

graph = builder.compile()