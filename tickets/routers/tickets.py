from fastapi import (APIRouter, 
                     HTTPException, status)
from schemas.ticket import Ticket, TicketCreate, TicketUpdate
import crud.tickets as crud
from typing import List
from utils.message import ErrorMessage, raise_if_error


router = APIRouter(prefix="/tickets",
                   responses={
                       400: {"model": ErrorMessage}
                   },
                   tags=["tickets"])


@router.get("/", response_model=List[Ticket])
async def list_tickets(limit: int = 27):
    tickets = await crud.get_tickets(limit=limit)
    return tickets


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate):
    new_ticket = await crud.create_ticket(ticket=ticket)
    return new_ticket


@router.get("/{pk}", response_model=Ticket)
async def get_single_ticket(pk: int):
    ticket = await crud.get_ticket(pk)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "incorrect ticket id"})
    return ticket


@router.put("/{pk}", response_model=Ticket)
async def update_ticket(pk: int, ticket: TicketUpdate):
    """
        Update ticket status.
    """
    new_ticket = await crud.update_ticket(ticket=ticket, ticket_id=pk)
    raise_if_error(new_ticket)
    return new_ticket
