from fastapi import FastAPI
from db.database import Base, engine
from routers import tickets, comments

app = FastAPI()
app.include_router(tickets.router)
app.include_router(comments.router)


@app.get("/")
async def index():
    return "why"
