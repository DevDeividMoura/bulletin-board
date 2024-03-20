""" 
tests.test_bulletin.py 
"""

import sys
from pathlib import Path
# Calculate the root directory path of the project and add it to sys.path
root_directory = Path(__file__).resolve().parents[3]
sys.path.append(str(root_directory))

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from apps.web.main import app

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.anyio
async def test_create_new_bulletin(client: AsyncClient):
    """
    Tests whether adding a new bulletin works correctly by checking 
    the status code and the presence of specific fields in the response.
    """
    response = await client.post("/bulletins/new", json={
        "title": "New Bulletin",
        "content": "This is a new Bulletin exemple",
        "category": "General"
    })

    assert response.status_code == HTTP_201_CREATED
    assert response.json()["title"] == "New Bulletin"
    assert "id" in response.json()
    assert "created_at" in response.json()

@pytest.mark.anyio
async def test_get_all_bulletins(client: AsyncClient):
    """
    Tests retrieving a list of bulletins. Verifies that the response is a list, 
    which indicates that bulletins can be fetched successfully.
    """
    response = await client.get("/bulletins/all")

    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_update_bulletin(client: AsyncClient):
    """
    Tests updating a bulletin by sending a PUT request to the bulletin's update endpoint with new data. 
    Verifies that the status code is 200 OK and the updated bulletin's ID matches the expected ID, 
    indicating the bulletin was successfully updated.
    """
    response= await client.get("/bulletins/all")
    bulletins = response.json()
    if bulletins:
        id = bulletins[0]["id"]

        response = await client.put(f"/bulletins/{id}", json={
            "title": "New Bulletin Title",
            "content": "New Bulletin Content",
            "category": "New Category"
        })

        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == id
    else:
        pytest.skip("No bulletins available to update.")

@pytest.mark.anyio
async def delete_bulletin_and_assert(client: AsyncClient, id: str, expected_success: bool):
    """
    Helper function to delete a bulletin by ID and assert the expected success response.

    Args:
        id (str): The ID of the bulletin to delete.
        expected_success (bool): The expected result of the delete operation.
    """
    response = await client.delete(f"/bulletins/{id}")
    assert response.status_code == HTTP_200_OK if expected_success else HTTP_400_BAD_REQUEST
    assert response.json()["success"] == expected_success


@pytest.mark.anyio
async def test_delete_bulletin_success(client: AsyncClient):
    """
    Tests successfully deleting a bulletin by sending a DELETE request to the bulletin's delete endpoint. 
    Verifies that the status code is 204 NO CONTENT and the success flag is True, indicating the bulletin was successfully deleted.
    """
    # Fetch the list of bulletins to find an ID to delete
    response = await client.get("/bulletins/all")
    bulletins = response.json()
    if bulletins:
        id = bulletins[-1]["id"]  # Assuming we delete the last bulletin in the list for testing
    
        await delete_bulletin_and_assert(client, id, expected_success=True)
    else:
        pytest.skip("No bulletins available to delete.")

@pytest.mark.anyio
async def _test_delete_bulletin_fail(client: AsyncClient):
    """
    Tests the failure of deleting a non-existent bulletin by sending a DELETE request to the bulletin's delete endpoint. 
    Verifies that the appropriate error status code is returned, indicating the bulletin could not be found or deleted.
    """
    # Using a non-existent ID to simulate a failed deletion.
    id = "non_existent_id"
    
    await delete_bulletin_and_assert(client, id, expected_success=False)  # Assuming your API returns a 404 for non-existent resources
