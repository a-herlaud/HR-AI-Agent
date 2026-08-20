import os
import requests


BASE_URL = os.getenv("FRONTEND_URL", "http://frontend:8080")


def test_frontend_homepage_serves_streamlit_shell() -> None:
    response = requests.get(BASE_URL, timeout=10)

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Streamlit" in response.text