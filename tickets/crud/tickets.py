from sqlalchemy import select, insert, update
from db.database import database
from models.ticket import Ticket, TicketStates
from schemas.ticket import TicketCreate, TicketUpdate
from typing import List, Union
from utils.message import ErrorMessage


async def get_tickets(limit: int = 27) -> List[Ticket]:
    query = select(Ticket).limit(limit)
    results = await database.fetch_all(query)
    return results


async def get_ticket_state(ticket_id: int) -> Union[TicketStates, ErrorMessage]:
    query = select(Ticket.state).where(Ticket.id == ticket_id)
    result = await database.fetch_one(query)
    if not result:
        return ErrorMessage(message="incorrect ticket_id")
    return result.get("state", default=None)


async def get_ticket(id: int) -> Ticket:
    query = select(Ticket).where(Ticket.id == id)
    result = await database.fetch_one(query)
    return result


async def create_ticket(ticket: TicketCreate) -> Ticket:
    query = insert(Ticket).values(title=ticket.title,
                                  email=ticket.email,
                                  description=ticket.description,
                                  state=TicketStates.opened)
    ticket_id = await database.execute(query)
    return await get_ticket(ticket_id)


async def update_ticket(ticket_id: int, ticket: TicketUpdate) -> Union[Ticket, ErrorMessage]:
    old_ticket = await get_ticket(ticket_id)

    # if ticket is not found
    if not old_ticket:
        return ErrorMessage(message="incorrect ticket id")

    # old_ticket.state is string, so we should convert it
    # to TicketStates
    old_ticket_state = TicketStates(old_ticket.state)

    # if we can't change state
    if not TicketStates.can_change_state(old_ticket_state, ticket.state):
        return ErrorMessage(message= \
                                f"cannot change state from {old_ticket_state.value} to {ticket.state.value}")

    query = update(Ticket).where(Ticket.id == ticket_id).values(**ticket.dict())
    await database.execute(query)

    return await get_ticket(ticket_id)
