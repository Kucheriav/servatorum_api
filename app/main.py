from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from app.logging_config import setup_logging
from app.database import engine, Base
from app.routers import (user_routes, company_routes, foundation_routes, fundraising_routes,
                         news_routes, wallet_routes, transaction_routes, sphere_routes)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # try:
    #     async with engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.create_all)
    # except Exception as e:
    #     print(f'DB error: {e}')
    #     raise
    yield
    await engine.dispose()


setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan, debug=True)
logger.info("FastAPI starting...")

app.include_router(company_routes.router, prefix="/company", tags=["company"])
app.include_router(foundation_routes.router, prefix="/foundation", tags=["foundation"])
app.include_router(fundraising_routes.router, prefix="/fundraising", tags=["fundraising"])
app.include_router(news_routes.router, prefix="/news", tags=["news"])
app.include_router(sphere_routes.router, prefix="/sphere", tags=["sphere"])
app.include_router(transaction_routes.router, prefix="/transaction", tags=["transaction"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(wallet_routes.router, prefix="/wallet", tags=["wallet"])
logger.info("Routers are connected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)