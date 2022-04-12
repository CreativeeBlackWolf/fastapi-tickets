from datetime import datetime
from pydantic import BaseModel, EmailStr
from utils.ormbase import OrmBase


class CommentBase(BaseModel):
    ticket_id: int
    text: str


class CommentCreate(CommentBase, OrmBase):
    email: EmailStr


class Comment(CommentBase, OrmBase):
    id: int
    created_on: datetime
    email: EmailStr

