"""
routers.bulletins.py
"""
from fastapi import APIRouter, Response, HTTPException, status
from typing import List, Optional

from apps.web.models.bulletins import (
    BulletinResponse,
    BulletinForm,
    Bulletins,
)
from constants import ERROR_MESSAGES

router = APIRouter()

@router.post("/new", response_model=Optional[BulletinResponse])
async def create_new_bulletin(form_data: BulletinForm, response: Response):
    """
    Creates a new bulletin based on the provided form data.
    If successful, returns the created bulletin with a status code of 201.
    If the operation fails due to invalid data, raises a 400 Bad Request error.

    Args:
        form_data (BulletinForm): The form data for creating a new bulletin.
        response (Response): The response object.

    Returns:
        Optional[BulletinResponse]: The created bulletin, if successful.
    """
    try:
        bulletin = Bulletins.create_new_bulletin(form_data)
        response.status_code = status.HTTP_201_CREATED
        return BulletinResponse(**bulletin.model_dump())

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_MESSAGES.DEFAULT()
        )

@router.get("/all", response_model=List[BulletinResponse])
async def get_all_bulletins():
    """
    Retrieves all bulletins from the database.
    Returns a list of bulletins.

    Returns:
        List[BulletinResponse]: A list of all bulletins.
    """
    return Bulletins.get_all_bulletins()

@router.put("/{id}", response_model=Optional[BulletinResponse])
async def update_bulletin_by_id(id: str, form_data: BulletinForm):
    """
    Updates an existing bulletin identified by the given ID with the provided form data.
    If the bulletin is successfully updated, returns the updated bulletin.
    If no bulletin with the given ID exists, raises a 401 Unauthorized error.

    Args:
        id (str): The ID of the bulletin to update.
        form_data (BulletinForm): The new data for the bulletin.

    Returns:
        Optional[BulletinResponse]: The updated bulletin, if successful.
    """
    bulletin = Bulletins.get_bulletin_by_id(id)
    if bulletin:
        update_bulletin = {**form_data.model_dump()}
        bulletin = Bulletins.update_bulletin_by_id(id, update_bulletin)
        return BulletinResponse(**bulletin.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )

@router.delete("/{id}")
async def create_new_bulletin(id: str, response: Response):
    """
    Deletes a bulletin identified by the given ID.
    If the bulletin is successfully deleted, sets the response status code to 204 No Content.
    Otherwise, does not modify the response.

    Args:
        id (str): The ID of the bulletin to delete.
        response (Response): The response object.
    """
    result = Bulletins.delete_bulletin_by_id(id)
    response.status_code = status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST
    return {"success": result}
