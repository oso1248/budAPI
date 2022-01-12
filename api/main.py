from fastapi import FastAPI
from . routers import admin, users

server = FastAPI()


@server.get("/", tags=['root'])
def root():
    return {"root": "API For Budweiser Brewing Department"}


server.include_router(admin.router)
server.include_router(users.router)
