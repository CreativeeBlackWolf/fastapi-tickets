from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate
from typing import List, Union
from utils.message import ErrorMessage


def get_comments(db: Session, limit: int = 27) -> List[Comment]:
    return db.query(Comment).limit(limit).all()


def create_comment(db: Session, comment: CommentCreate) -> Union[Comment, ErrorMessage]:
    db_comment = Comment(ticket_id=comment.ticket_id,
                         text = comment.text,
                         email=comment.email)

    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except IntegrityError:
        return ErrorMessage(message=f"ticket with ticket_id {comment.ticket_id} is not present.")
