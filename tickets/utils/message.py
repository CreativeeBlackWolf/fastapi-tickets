from pydantic import BaseModel


class ErrorMessage(BaseModel):
    error: str = "error"
    message: str
