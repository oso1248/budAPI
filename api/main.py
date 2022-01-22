from fastapi import FastAPI
from . routers import rte_auth, rte_users, rte_jobs, rte_suppliers, rte_commodities, rte_brands
from .database.database import engine
from . models import mdl_user, mdl_jobs, mdl_suppliers, mdl_commodities, mdl_brands
from . config import settings


mdl_user.Base.metadata.create_all(bind=engine)
mdl_jobs.Base.metadata.create_all(bind=engine)
mdl_suppliers.Base.metadata.create_all(bind=engine)
mdl_commodities.Base.metadata.create_all(bind=engine)
mdl_brands.Base.metadata.create_all(bind=engine)


server = FastAPI()


@server.get("/", tags=['root'], include_in_schema=False)
def root():
    return {"root": "API For Fort Collins Budweiser Brewing Department"}


server.include_router(rte_auth.router)
server.include_router(rte_users.router)
server.include_router(rte_jobs.router)
server.include_router(rte_suppliers.router)
server.include_router(rte_commodities.router)
server.include_router(rte_brands.router)
