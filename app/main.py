from fastapi import FastAPI
from app.routers import user_routes, legal_entity_routes, fundraising_routes
from app.db_management import init_db


# init_db()
app = FastAPI()
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(legal_entity_routes.router, prefix="/legal_entity", tags=["legal_entity"])
app.include_router(fundraising_routes.router, prefix="/fundraising", tags=["fundraising"])




