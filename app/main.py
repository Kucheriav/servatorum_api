from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user_routes, legal_entity_routes, fundraising_routes, news_routes


app = FastAPI()
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(legal_entity_routes.router, prefix="/legal_entity", tags=["legal_entity"])
app.include_router(fundraising_routes.router, prefix="/fundraising", tags=["fundraising"])
app.include_router(news_routes.router, prefix="/news", tags=["news"])


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print('-----')
        print(e)
        raise


@app.on_event("startup")
async def startup_event():
    await create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)