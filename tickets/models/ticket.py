import enum
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, ChoiceType
from db.database import Base


class TicketStates(enum.Enum):
    opened = "opened"
    on_review = "on review"
    answered = "answered"
    closed = "closed"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    email = Column(EmailType, nullable=False)
    state = Column(ChoiceType(TicketStates), default=TicketStates.opened, nullable=False)


    def __repr__(self):
        return f"<Ticket(title={self.title})>"
