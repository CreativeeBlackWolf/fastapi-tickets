from __future__ import annotations
import enum
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, ChoiceType
from db.database import Base


class TicketStates(enum.Enum):
    """
        Ticket is created in "opened" status.\n
        Can go to "answered" or "closed" status from "opened".\n
        Can go to "pending" or "closed" status from "answered".\n
        "Closed" status is final (can't change status or add comments).\n
    """
    opened = "opened"
    answered = "answered"
    pending = "pending"
    closed = "closed"

    @staticmethod
    def __priority(state: TicketStates):
        return list(TicketStates).index(TicketStates(state))

    @classmethod
    def can_change_state(cls, fromState: TicketStates, toState: TicketStates) -> bool:
        if fromState is cls.pending and toState is cls.answered:
            return True
        if fromState is cls.opened and toState is cls.pending:
            return False
        if cls.__priority(fromState) >= cls.__priority(toState):
            return False
        return True


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    email = Column(EmailType, nullable=False)
    state = Column(ChoiceType(TicketStates), default=TicketStates.opened, nullable=False)
    comments = relationship("Comment",
                            back_populates="ticket",
                            # lazy="dynamic",
                            # primaryjoin="Ticket.id == Comment.ticket_id"
                            )

    def __repr__(self):
        return f"<Ticket(title={self.title})>"


tickets = Ticket.__table__
