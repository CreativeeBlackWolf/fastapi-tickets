from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy import select, insert
from models.comment import Comment
from schemas.comment import CommentCreate
from typing import List, Union
from db.database import database
from utils.message import ErrorMessage


async def get_comments(limit: int = 27) -> List[Comment]:
    query = select(Comment).limit(limit)
    return await database.fetch_all(query)

async def get_ticket_comments(pk: int) -> List[Comment]:
    query = select(Comment).where(Comment.ticket_id == pk)
    results = await database.fetch_all(query)
    return results

async def get_comment(pk: int) -> Comment:
    query = select(Comment).where(Comment.id == pk)
    results = await database.fetch_one(query)
    return results

async def create_comment(comment: CommentCreate) -> Union[Comment, ErrorMessage]:
    query = insert(Comment)\
        .values(text=comment.text,
        ticket_id=comment.ticket_id,
        email=comment.email)

    try:
        id = await database.execute(query)
        return await get_comment(id)
    except ForeignKeyViolationError:
        return ErrorMessage(message=f"ticket_id ({comment.ticket_id}) is not found.")
