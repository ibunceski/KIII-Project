from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch('main.collection')
def test_add_item(mock_collection):
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "507f1f77bcf86cd799439011"
    mock_collection.insert_one = AsyncMock(return_value=mock_insert_result)

    mock_collection.find_one = AsyncMock(return_value={
        "_id": "507f1f77bcf86cd799439011",
        "name": "testitem",
        "quantity": 5
    })

    new_item = {"name": "testitem", "quantity": 5}
    response = client.post("/api/items", json=new_item)

    assert response.status_code == 200
    assert response.json()["name"] == "testitem"
    assert response.json()["quantity"] == 5


@patch('main.collection')
def test_delete_item(mock_collection):
    mock_collection.find_one = AsyncMock(return_value={
        "_id": "507f1f77bcf86cd799439011",
        "name": "todelete",
        "quantity": 1
    })
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_collection.delete_one = AsyncMock(return_value=mock_delete_result)

    response = client.delete("/api/items/507f1f77bcf86cd799439011")

    assert response.status_code == 200


@patch('main.collection')
def test_get_items(mock_collection):
    mock_items = [
        {"_id": "507f1f77bcf86cd799439011", "name": "item1", "quantity": 5},
        {"_id": "507f1f77bcf86cd799439012", "name": "item2", "quantity": 3}
    ]

    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=mock_items)
    mock_collection.find.return_value = mock_cursor

    response = client.get("/api/items")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "item1"
    assert response.json()[1]["name"] == "item2"
