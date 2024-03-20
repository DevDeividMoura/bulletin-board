"""
models.bulletins.py
"""
from datetime import datetime, timezone
from peewee import (
    CharField,
    TextField,
    DateTimeField,
    Model,
)
from pydantic import BaseModel
from typing import Optional, List
from playhouse.shortcuts import model_to_dict

import uuid

from apps.web.internal.db import DB


class Bulletin(Model):
    """
    Represents the structure of the "bulletins" table in the database.
    """
    id = CharField(primary_key=True, unique=True)
    title = CharField()
    content = TextField()
    category = CharField()
    created_at = DateTimeField()

    class Meta:
        database = DB


class BulletinModel(BaseModel):
    """
    Pydantic model for validating and representing bulletin data.
    """
    id: str
    title: str
    content: str
    category: str
    created_at: str


class BulletinForm(BaseModel):
    """
    Pydantic model for incoming bulletin form data.
    """
    title: str
    content: str
    category: str


class BulletinResponse(BaseModel):
    """
    Pydantic model for the response containing bulletin data.
    """
    id: str
    title: str
    content: str
    category: str
    created_at: str


class BulletinTable:
    """
    Provides database operations related to bulletins.
    """
    def __init__(self, db):
        self.db = db
        db.create_tables([Bulletin], safe=True)

    def create_new_bulletin(self, form_data: BulletinForm) -> Optional[BulletinModel]:
        """
        Creates a new bulletin in the database based on the provided form data.

        Raises:
            ValidationError: If the form data is invalid.
        """
        data = {**form_data.model_dump()}
        data["id"] = uuid.uuid4().hex
        data["created_at"] = datetime.now(timezone.utc).isoformat()
        bulletin = BulletinModel(
            **data
        )
        result = Bulletin.create(**bulletin.model_dump())
        return bulletin if result else None

    def get_all_bulletins(self) -> List[BulletinModel]:
        """
        Returns a list of all bulletins from the database, ordered by creation date (descending).
        """
        bulletins = Bulletin.select().order_by(Bulletin.created_at.desc())
        return [BulletinModel(**model_to_dict(bulletin)) for bulletin in bulletins]

    def get_bulletin_by_id(self, id: str) -> Optional[BulletinModel]:
        """
        Retrieves a bulletin by its ID from the database.
        """
        bulletin = Bulletin.get(Bulletin.id == id)
        return BulletinModel(**model_to_dict(bulletin))

    def update_bulletin_by_id(self, id: str, bulletin_data: dict) -> Optional[BulletinModel]:
        """
        Updates an existing bulletin based on the provided ID and data.

        Raises:
            IntegrityError: If the update violates database constraints (e.g., unique title).
        """
        try:
            query = Bulletin.update(**bulletin_data).where(Bulletin.id == id)
            query.execute()
            bulletin = Bulletin.get_by_id(id)
            return BulletinModel(**model_to_dict(bulletin))
        except Exception as e:
            print(e)
            return None

    def delete_bulletin_by_id(self, id: str) -> bool:
        """
        Deletes a bulletin from the database based on its ID.

        Returns:
            True if the bulletin was deleted successfully, False otherwise.
        """
        query = Bulletin.delete().where(Bulletin.id == id)
        return query.execute() > 0


Bulletins = BulletinTable(DB)
