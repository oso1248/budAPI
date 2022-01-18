from fastapi import FastAPI
from . routers import rte_auth, rte_users, rte_jobs, rte_suppliers, rte_commodities
from .database.database import engine
from . models import mdl_user, mdl_jobs, mdl_suppliers, mdl_commodities

mdl_user.Base.metadata.create_all(bind=engine)
mdl_jobs.Base.metadata.create_all(bind=engine)
mdl_suppliers.Base.metadata.create_all(bind=engine)
mdl_commodities.Base.metadata.create_all(bind=engine)

# insert into users table on startup
# INSERT INTO users (name, username, role, password, created_by, updated_by, brewery, permissions) VALUES ('admin', 'admin', 'Admin', 'BudAdmin1!', 1, 1, 'FTC', 6)

server = FastAPI()


@server.get("/", tags=['root'], include_in_schema=False)
def root():
    return {"root": "API For Fort Collins Budweiser Brewing Department"}


server.include_router(rte_auth.router)
server.include_router(rte_users.router)
server.include_router(rte_jobs.router)
server.include_router(rte_suppliers.router)
server.include_router(rte_commodities.router)
