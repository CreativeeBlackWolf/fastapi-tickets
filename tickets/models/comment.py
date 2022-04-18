from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType
from db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(ForeignKey("tickets.id"))
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(EmailType, nullable=False)
    text = Column(String(), nullable=False)

    ticket = relationship("Ticket", 
                          back_populates="comments"
                          )

comments = Comment.__table__
