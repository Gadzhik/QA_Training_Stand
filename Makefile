PY = python
VENV_PATH = .venv
BIN = $(VENV_PATH)/Scripts

.PHONY: install up down

install:
	$(PY) -m venv $(VENV_PATH)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .
	$(BIN)/python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/delivery.proto

up:
	docker-compose up -d --build

down:
	docker-compose down
