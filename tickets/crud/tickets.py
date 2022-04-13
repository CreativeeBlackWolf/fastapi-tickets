from sqlalchemy.orm import Session
from models.ticket import Ticket, TicketStates
from schemas.ticket import TicketCreate, TicketUpdate
from typing import List, Union
from utils.message import ErrorMessage


def get_tickets(db: Session, limit: int = 27) -> List[Ticket]:
    return db.query(Ticket).limit(limit).all()

def get_ticket(db: Session, id: int) -> Ticket:
    return db.query(Ticket).filter(Ticket.id == id).one_or_none()

def create_ticket(db: Session, ticket: TicketCreate) -> Ticket:
    db_ticket = Ticket(title=ticket.title, 
                       email=ticket.email, 
                       description=ticket.description)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdate) -> Union[Ticket, ErrorMessage]:
    db_ticket = db.get(Ticket, ticket_id)
    if not db_ticket:
        return ErrorMessage(message="incorrect ticket id")
    ticket_data = ticket.dict(exclude_unset=True)
    
    # if we can't change state of ticket
    if not TicketStates.can_change_state(db_ticket.state, ticket.state):
        return ErrorMessage(message=f"cannot change state from {db_ticket.state} to {ticket.state}")

    for key, value in ticket_data.items():
        setattr(db_ticket, key, value) if value else None
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
