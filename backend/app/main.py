from fastapi import FastAPI
from app.routers import users, todos

app = FastAPI()

app.include_router(users.router)
app.include_router(todos.router)
