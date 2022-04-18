from fastapi import (APIRouter,
                     HTTPException, status)
from schemas.comment import Comment, CommentCreate
import crud.comments as crud
from typing import List
from crud.tickets import get_ticket_state
from models.ticket import TicketStates
from utils.message import ErrorMessage, raise_if_error


router = APIRouter(prefix="/comments",
                   responses={
                       400: {"model": ErrorMessage}
                   },
                   tags=["comments"])


@router.get("/", response_model=List[Comment])
async def list_comments(limit: int = 27):
    return await crud.get_comments(limit=limit)


@router.get("/by_ticket", response_model=List[Comment])
async def get_comments_by_ticket(pk: int):
    return await crud.get_ticket_comments(pk)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate):
    state = await get_ticket_state(comment.ticket_id)
    raise_if_error(state)

    if state is TicketStates.closed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=ErrorMessage(
                                message="ticket is in closed state"
                                ).dict()
                            )
    
    new_comment = await crud.create_comment(comment=comment)
    raise_if_error(new_comment)

    return new_comment
