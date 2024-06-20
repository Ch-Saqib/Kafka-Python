from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
from sqlmodel import Field, SQLModel
from typing import List, Optional
import todo_pb2


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str


async def consume(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.value)
            # Decrialized Data
            get_data = todo_pb2.Todo_Proto()
            get_data.ParseFromString(msg.value)
            print(f"Decrialized Data : ", get_data)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


def lifespan(app: FastAPI):
    print("Consumer Start ....")
    asyncio.create_task(consume(topic="todos", bootstrap_servers="broker:19092"))
    yield


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/")
def get():
    return {"message": "Hello World"}


@app.post("/add_data")
async def add_data_kafka(todo: Todo):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        add_data = todo_pb2.Todo_Proto(
            name=todo.name,
            description=todo.description,
        )
        # Serialize Data
        protoc_data = add_data.SerializeToString()
        print(f"Serialized Data : ", protoc_data)
        # Produce message
        await producer.send_and_wait(topic="todos", value=protoc_data)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()
    return todo.model_dump_json()
