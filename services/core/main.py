import asyncio
import json
from fastapi import FastAPI, Response
from strawberry.fastapi import GraphQLRouter
from services.core.graphql.schema import schema
from prometheus_fastapi_instrumentator import Instrumentator
from aiokafka import AIOKafkaProducer

app = FastAPI(title="Polyglot QA Core")

# 1. GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# 2. REST
@app.post("/api/users")
async def create_user(username: str):
    # Kafka Integration
    producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')
    try:
        await producer.start()
        msg = json.dumps({"event": "USER_CREATED", "username": username}).encode('utf-8')
        await producer.send_and_wait("user_events", msg)
    except Exception as e:
        print(f"Values Kafka Error: {e}") # Don't block app if kafka is not ready yet
    finally:
        await producer.stop()
        
    return {"status": "created", "username": username}

# 3. SOAP (Mock)
@app.post("/soap/currency")
async def soap_currency(request: str = ""):
    # Very basic XML response simulation
    xml = """
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetRateResponse>
          <Rate>USD/EUR: 0.92</Rate>
        </GetRateResponse>
      </soap:Body>
    </soap:Envelope>
    """
    return Response(content=xml, media_type="application/xml")

# 4. Observability
Instrumentator().instrument(app).expose(app)
