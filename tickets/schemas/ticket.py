from datetime import datetime
from typing import List
from schemas.comment import Comment
from models.ticket import TicketStates
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel
from utils.ormbase import OrmBase

class TicketBase(BaseModel):
    title: str
    description: str


class TicketUpdate(SQLModel):
    state: TicketStates


class TicketCreate(TicketBase):
    email: EmailStr


class Ticket(TicketBase, OrmBase):
    id: int
    created_on: datetime
    updated_on: datetime
    email: EmailStr
    state: TicketStates
    comments: List[Comment]
