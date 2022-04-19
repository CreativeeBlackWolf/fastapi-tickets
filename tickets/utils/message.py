from typing import Any
from pydantic import BaseModel
from fastapi import HTTPException, status


class ErrorMessage(BaseModel):
    error: str = "error"
    message: str


def raise_if_error(var: Any, status_code=status.HTTP_400_BAD_REQUEST):
    if isinstance(var, ErrorMessage):
        raise HTTPException(status_code=status_code,
                            detail={**var.dict()})
