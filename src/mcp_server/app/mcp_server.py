from fastmcp import FastMCP
import requests
from ddgs import DDGS
from bs4 import BeautifulSoup

mcp = FastMCP("HR MCP")

@mcp.tool()
def get_quarter_kpis() -> dict:
    """
    get the HR KPIs for the current quarter
    """

    response = requests.get(
    "http://kpi-api:8000/api"
    )

    return response.json()

@mcp.tool()
def get_monthly_kpis(month: str) -> dict:
    """
    get the HR KPIs for a certain month
    """
    month = month.capitalize()
    response = requests.get(
    f"http://kpi-api:8000/api/months/{month}"
    )

    return response.json()

@mcp.tool()
def web_search(query: str) -> list[dict]:
    """
    Search the internet for current and external information.

    MUST be used for:
    - current date/time
    - latest news or events
    - recent documentation
    - information that may have changed after model training

    Returns search results containing titles, URLs, and snippets.

    If a result needs deeper analysis, use fetch_url with the returned URL.
    Do not answer using your memory when web information is required.
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

        return [
            {
                "title": r["title"],
                "url": r["href"],
                "description": r["body"],
            }
            for r in results
        ]

@mcp.tool()
def fetch_url(url: str) -> str:
    """
    Extract the readable text content from a webpage URL.

    MUST be used after web_search when:
    - the search result snippet is not enough
    - you need details from the actual webpage
    - you need to verify information from a source
    - you need to summarize or analyze a webpage

    Do not invent webpage content. Always fetch the URL before using
    information from that page.
    """

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.get_text(
        separator="\n",
        strip=True
    )

mcp.run(
    transport="http",
    host="0.0.0.0",
    port=8001,
)