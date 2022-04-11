# Import all the models, so that Base has them before being
from db.database import Base
from models.ticket import Ticket
from models.comment import Comment