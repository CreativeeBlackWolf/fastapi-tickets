from fastapi import FastAPI
from db.database import Base, engine
from routers import tickets

app = FastAPI()
app.include_router(tickets.router)


@app.get("/")
async def index():
    return "why"
