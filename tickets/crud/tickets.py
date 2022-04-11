from sqlalchemy.orm import Session
from models.ticket import Ticket
from schemas.ticket import TicketCreate, TicketUpdate
from typing import List


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

def update_ticket(db: Session, ticket_id: int, ticket: TicketUpdate) -> Ticket:
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).one_or_none()

    if not db_ticket:
        return None

    for var, value in vars(ticket).items():
        setattr(db_ticket, var, value) if value else None

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
