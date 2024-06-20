from todo.main import Session, get_data, app, create_engine
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

load_dotenv()


conn_str = os.getenv("TEST_DATABASE")
engine = create_engine(conn_str)


def test_get_data():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_data] = test_get_data

client = TestClient(app)


def test_get_data():
    response = client.get("/todo")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_data():
    new_data = {"name": "John Doe", "description": "This is John Doe"}
    response = client.post("/todo/add", json=new_data)
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["description"] == "This is John Doe"


def test_update_data():
    new_data = {"name": "John Doe", "description": "This is John Doe"}
    response = client.post("/todo/add/37", json=new_data)
    update_data = {"name": "Jane Doe", "description": "This is Jane Doe"}
    response = client.put("/todo/update/37", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"
    assert response.json()["description"] == "This is Jane Doe"


def test_delete_data():
    response = client.delete("/todo/delete/34")
    assert response.status_code == 200
    