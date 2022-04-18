from fastapi import FastAPI
from db.database import database
from routers import tickets, comments
from fastapi.responses import RedirectResponse


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def index():
    return RedirectResponse("/docs")


app.include_router(tickets.router)
app.include_router(comments.router)