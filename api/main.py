from fastapi import FastAPI
from .routers import users

server = FastAPI()


@server.get("/", tags=['root'])
def root():
    return {"root": "API For Budweiser Brewing Department"}


server.include_router(users.router)
