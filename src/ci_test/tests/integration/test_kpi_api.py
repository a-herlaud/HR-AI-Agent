import os
import pytest
import requests


BASE_URL = os.getenv("KPI_API_URL", "http://kpi-api:8000")


@pytest.mark.parametrize(
    "path",
    [
        "/api/kpis",
        "/api/quarters/Q1",
        "/api/months/Janvier",
        "/api/employees/Pauline",
    ],
)
def test_kpi_api_endpoints_return_json_lists(path: str) -> None:
    response = requests.get(f"{BASE_URL}{path}", timeout=10)

    assert response.status_code == 200
    assert isinstance(response.json(), list)