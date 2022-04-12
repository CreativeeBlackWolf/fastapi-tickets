from os import stat
from fastapi import (APIRouter, Depends, 
                     HTTPException, status)
from schemas.comment import Comment, CommentCreate
import crud.comments as crud
from sqlalchemy.orm import Session
from typing import List
from dependencies import get_db
from utils.message import ErrorMessage


router = APIRouter(prefix="/comments",
                   responses={
                       400: {"model": ErrorMessage}
                    },
                    tags=["comments"])


@router.get("/", response_model=List[Comment])
async def list_comments(db: Session = Depends(get_db), limit: int = 27):
    return crud.get_comments(db, limit=limit)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = crud.create_comment(db, comment)
    if isinstance(new_comment, ErrorMessage):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail={new_comment.error: new_comment.message})
    return new_comment
