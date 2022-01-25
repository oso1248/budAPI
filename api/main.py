from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . routers import rte_auth, rte_users, rte_jobs, rte_suppliers, rte_commodities, rte_brands, rte_inv_material
from . config import settings
from .metadata import description, tags_metadata
from .oauth2.oauth2 import get_current_user
from . validators import val_user
from loguru import logger
import sys

# logger.remove()
# logger.add(sys.stdout, colorize=True,
#            format="<green>{time}</green> <level>{message}</level>", backtrace=False, diagnose=True)

# logger.add("logs/main.log", rotation="2 week",
#            backtrace=False, diagnose=True)

# logger.add("logs/rte_inv_main.log", rotation="2 week",
#            backtrace=False, diagnose=True, filter='rte_inv_material.py')


server = FastAPI(
    title="Bud Brewing API 🇺🇲",
    description=description,
    version="0.0.1",
    terms_of_service="https://github.com/oso1248/budAPI/blob/master/LICENSE",
    contact={
        "name": "Adam Coulson",
        "url": "https://github.com/oso1248/budAPI",
        "email": "oso1248@gmail.com",
    },
    license_info={
        "name": "MIT License Copyright (c) 2022 Adam Coulson",
        "url": "https://github.com/oso1248/ftc_brewing/blob/master/LICENSE",
    }, openapi_tags=tags_metadata
)

origins = ['*', 'https://www.google.com/']

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Checks If User Is Logged In
@server.get("/", tags=['Root'], include_in_schema=False)
def root(current_user: val_user.UserOut = Depends(get_current_user)):
    return {"root": "Logged In"}


server.include_router(rte_auth.router)
server.include_router(rte_users.router)
server.include_router(rte_jobs.router)
server.include_router(rte_suppliers.router)
server.include_router(rte_commodities.router)
server.include_router(rte_brands.router)
server.include_router(rte_inv_material.router)
