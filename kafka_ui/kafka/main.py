from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from contextlib import asynccontextmanager
import asyncio


KAFKA_TOPIC = "Topic"
KAFKA_SERVER = "broker:19092"
KAFKA_GROUP_ID = "group_id"


async def consumer():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

@asynccontextmanager
def lifespan(app:FastAPI):
    print("Create Connsumer")
    asyncio.create_task(consumer())
    print("Created")
    yield


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "Hello World"}
