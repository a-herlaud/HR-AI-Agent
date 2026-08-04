FROM python:3.13-slim-trixie@sha256:6771159cd4fa5d9bba1258caf0b82e6b73458c694d178ad97c5e925c2d0e1a91

WORKDIR /app

COPY requirements.txt .
COPY app/ .

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["opentelemetry-instrument", "python", "mcp_server.py"]