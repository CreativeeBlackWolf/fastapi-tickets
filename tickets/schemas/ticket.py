from datetime import datetime
from pydantic import BaseModel, EmailStr
from models.ticket import TicketStates
from sqlmodel import SQLModel


class TicketBase(BaseModel):
    title: str
    description: str


class TicketUpdate(SQLModel):
    state: TicketStates


class TicketCreate(TicketBase):
    email: EmailStr


class Ticket(TicketBase):
    id: int
    created_on: datetime
    updated_on: datetime
    email: EmailStr
    state: TicketStates

    class Config:
        orm_mode = True
