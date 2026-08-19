import os
import requests
import json

BASE_URL = os.getenv("MCP_SERVER_URL", "http://host.docker.internal:8001")


def test_mcp_initialize() -> None:
    response = requests.post(
        f"{BASE_URL}/mcp",
        headers={"Accept": "application/json, text/event-stream"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "1.0"},
            },
        },
        timeout=10,
    )

    assert response.status_code == 200

    payload = json.loads(
        next(line[6:] for line in response.text.splitlines() if line.startswith("data:"))
    )

    assert payload["jsonrpc"] == "2.0"
    assert payload["id"] == 1
    assert "result" in payload