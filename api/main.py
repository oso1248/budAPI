from . routers import rte_auth, rte_brands_brewing, rte_brands_finishing, rte_brands_packaging
from . routers import rte_users, rte_jobs, rte_suppliers, rte_commodities, rte_inv_material
from . routers import rte_inv_hop, rte_inv_combned, rte_manpower, rte_commodity_usage
from fastapi.middleware.cors import CORSMiddleware
from .metadata import description, tags_metadata
from .oauth2.oauth2 import get_current_user
from fastapi import FastAPI, Depends
from . validators import val_user
from . config import settings
from loguru import logger


logger.add("logs/main.log", rotation="2 weeks",
           backtrace=False, diagnose=True)

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
        "url": "https://github.com/oso1248/budAPI/blob/master/LICENSE",
    }, swagger_ui_parameters={"syntaxHighlight": False}, openapi_tags=tags_metadata, redoc_url=None
)


origins = ['*', 'https://www.google.com/']
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root
@logger.catch()
@ server.get("/", tags=['Root'], include_in_schema=False)
def root():
    return {"root": "Bud API"}


# Checks If User Is Logged In
@server.get("/logcheck", include_in_schema=False)
def log_check(current_user: val_user.UserOut = Depends(get_current_user)):
    return {'detail': 'logged'}


server.include_router(rte_auth.router)
server.include_router(rte_users.router)
server.include_router(rte_jobs.router)
server.include_router(rte_suppliers.router)
server.include_router(rte_commodities.router)
server.include_router(rte_commodity_usage.router)
server.include_router(rte_brands_brewing.router)
server.include_router(rte_brands_finishing.router)
server.include_router(rte_brands_packaging.router)
server.include_router(rte_inv_material.router)
server.include_router(rte_inv_hop.router)
server.include_router(rte_inv_combned.router)
server.include_router(rte_manpower.router)
