from fastapi import (APIRouter, Depends, 
                     HTTPException, status)
from schemas.ticket import Ticket, TicketCreate, TicketUpdate
import crud.tickets as crud
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from utils.message import ErrorMessage


router = APIRouter(prefix="/tickets",
                   responses={
                       400: {"model": ErrorMessage}
                    },
                    tags=["tickets"])


@router.get("/", response_model=List[Ticket])
def list_tickets(limit: int = 27, db: Session = Depends(get_db)):
    tickets = crud.get_tickets(db, limit=limit)
    return tickets


@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = crud.create_ticket(db, ticket=ticket)
    return new_ticket


@router.get("/{pk}", response_model=Ticket)
def get_single_ticket(pk: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket(db, id=pk)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"error": "incorrect ticket id"})
    return ticket


@router.put("/{pk}", 
            response_model=Ticket, 
            responses={
                400: {"model": ErrorMessage}
                })
def update_ticket(pk: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    """
        Update ticket status.
    """
    new_ticket = crud.update_ticket(db, ticket=ticket, ticket_id=pk)
    if isinstance(new_ticket, ErrorMessage):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={new_ticket.error: new_ticket.message})
    return new_ticket
