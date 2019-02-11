"""Users db models."""
from sqlalchemy import Column, Integer, String, Unicode
from marshmallow import Schema, fields, post_load
from src.models.base import Base
import uuid


class Users(Base):
    """Users database model."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    user_secret = Column(Unicode(), nullable=False,
                         default=lambda: str(uuid.uuid4()))


class UsersSchema(Schema):
    """Schema for the Users Model."""

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    user_secret = fields.Raw()

    @post_load
    def create_user(self, data):
        """Create a User Object."""
        return Users(**data)
