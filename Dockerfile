FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    zlib1g-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY protos/ protos/
COPY services/ services/
# Generate Proto code
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/delivery.proto

CMD ["python", "services/run.py"]
