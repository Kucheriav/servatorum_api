from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.news_crud import NewsCRUD
from app.schemas.news_schema import *

router = APIRouter()
news_crud = NewsCRUD()

@router.post("/create_news", response_model=NewsResponse)
async def create_news(news: NewsCreate):
    try:
        return await news_crud.create_news(news)
    except ValidationError as e:
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Ошибка уникальности")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_news/{news_id}", response_model=NewsResponse)
async def get_news(news_id: int):
    news_item = await news_crud.get_news(news_id)
    if news_item:
        return news_item
    raise HTTPException(status_code=404, detail="Новость не найдена")

@router.get("/get_news_pages", response_model=NewsPaginationResponse)
async def get_news(page: int = 1, page_size: int = 10):
    result = await news_crud.get_news_paginated(page=page, page_size=page_size)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Новости не найдены")

@router.patch("/update_news/{news_id}", response_model=NewsResponse)
async def update_news(news_id: int, news_params_to_update: NewsUpdate):
    updated_news = await news_crud.update_news(news_id, news_params_to_update)
    if updated_news:
        return updated_news
    raise HTTPException(status_code=404, detail="Новость не найдена")

@router.delete("/delete_news/{news_id}")
async def delete_news(news_id: int):
    if await news_crud.delete_news(news_id):
        return {"message": "Новость удалена"}
    raise HTTPException(status_code=404, detail="Новость не найдена")
