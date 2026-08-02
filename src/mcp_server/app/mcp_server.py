from fastmcp import FastMCP
import requests

mcp = FastMCP("HR MCP")

@mcp.tool()
def get_quarter_kpis() -> dict:
    """
    get the HR KPIs for the current quarter
    """

    response = requests.get(
    "http://host.docker.internal:8000/api"
    )

    return reponse.json()

@mcp.tool()
def get_monthly_kpis(month: str) -> dict:
    """
    get the HR KPIs for a certain month
    """

    response = requests.get(
    "http://host.docker.internal:8000/api/{month}"
    )

    return reponse.json()

mcp.run(
    transport="http",
    host="0.0.0.0",
    port=8001,
)