""" 
tests/test_bulletin.py 
"""
import sys
from pathlib import Path

# Calculate the root directory path of the project and add it to sys.path
root_directory = Path(__file__).resolve().parents[3]
sys.path.append(str(root_directory))

from apps.web.main import app
from fastapi.testclient import TestClient

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

client = TestClient(app)

def test_create_bulletin():
    """
    Tests whether adding a new bulletin works correctly by checking 
    the status code and the presence of specific fields in the response.
    """
    response = client.post("/bulletins/new", json={
        "title": "New Bulletin",
        "content": "This is a new Bulletin exemple",
        "category": "General"
    })

    assert response.status_code == HTTP_201_CREATED
    assert response.json()["title"] == "New Bulletin"
    assert "id" in response.json()
    assert "created_at" in response.json()

def test_get_bulletins():
    """
    Tests retrieving a list of bulletins. Verifies that the response is a list, 
    which indicates that bulletins can be fetched successfully.
    """
    response = client.get("/bulletins")

    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list)

def test_update_bulletin():
    """
    Tests updating a bulletin by sending a PUT request to the bulletin's update endpoint with new data. 
    Verifies that the status code is HTTP_200_OK and the updated bulletin's ID matches the expected ID, 
    indicating the bulletin was successfully updated.
    """
    id = 1  # Note: This ID should correspond to an existing bulletin in your testing database.
    response = client.put(f"/bulletins/{id}/update", json={
        "title": "New Bulletin Title",
        "content": "New Bulletin Content",
        "category": "New Category"
    })

    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == id

def test_delete_bulletin():
    """
    Tests deleting a bulletin by sending a DELETE request to the bulletin's delete endpoint. 
    Verifies that the status code is HTTP_204_NO_CONTENT, indicating the bulletin was successfully deleted.
    """
    id = 1  # Note: This ID should correspond to an existing bulletin in your testing database.
    response = client.delete(f"/bulletins/{id}/delete")
    assert response.status_code == HTTP_204_NO_CONTENT
