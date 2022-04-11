from datetime import datetime
from pydantic import BaseModel, EmailStr
from models.ticket import TicketStates


class TicketBase(BaseModel):
    title: str
    description: str


class TicketUpdate(BaseModel):
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
