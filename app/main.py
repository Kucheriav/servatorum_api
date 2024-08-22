from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, funds, collections, posts, complaints

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(funds.router, prefix="/funds", tags=["funds"])
app.include_router(collections.router, prefix="/collections", tags=["collections"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(complaints.router, prefix="/complaints", tags=["complaints"])