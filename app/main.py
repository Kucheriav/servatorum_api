from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
from app.logging_config import setup_logging
from app.database import engine, Base
from app.routers import (user_routes, company_routes, foundation_routes, fundraising_routes,
                         news_routes, wallet_routes, transaction_routes, sphere_routes)

from app.scripts_utlis.bot_sms_code_sender import start_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = asyncio.create_task(start_bot())
    yield
    await engine.dispose()
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass


setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan, debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены (для тестирования)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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