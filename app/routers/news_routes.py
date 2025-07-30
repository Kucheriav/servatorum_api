from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from sqlalchemy import exc
from app.crud.news_crud import NewsCRUD
from app.schemas.news_schema import *
from app.scripts_utils.dependencies import get_current_user, get_current_admin
import logging

router = APIRouter()
news_crud = NewsCRUD()

# Create a logger specific to this module
logger = logging.getLogger("app.news_router")

@router.post("/create_news", response_model=NewsResponse)
async def create_news(news: NewsCreate, current_user=Depends(get_current_user)):
    logger.info(f"{current_user.phone} creates news")
    try:
        result = await news_crud.create_news(news=news)
        logger.info("News created successfully")
        return result
    except ValidationError as e:
        logger.error("Validation error while creating news", exc_info=True)
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error['loc'][-1]
            message = error['msg']
            error_messages.append(f"Ошибка в поле '{field}': {message}")
        raise HTTPException(status_code=422, detail=error_messages)
    except exc.IntegrityError:
        logger.error("Integrity error: uniqueness constraint violated")
        raise HTTPException(status_code=400, detail="Ошибка уникальности")
    except Exception as e:
        logger.error("Unexpected error while creating news", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get_news/{news_id}", response_model=NewsResponse)
async def get_news(news_id: int):
    logger.info(f"Request received to get news with ID: {news_id}")
    news_item = await news_crud.get_news(news_id=news_id)
    if news_item:
        logger.info(f"News item with ID {news_id} retrieved successfully")
        return news_item
    logger.warning(f"News item with ID {news_id} not found")
    raise HTTPException(status_code=404, detail="Новость не найдена")

@router.get("/get_news_pages", response_model=NewsPaginationResponse)
async def get_news(page: int = 1, page_size: int = 10):
    logger.info(f"Request received to get news paginated: Page {page}, Page Size {page_size}")
    result = await news_crud.get_news_paginated(page=page, page_size=page_size)
    if result:
        logger.info(f"News page {page} retrieved successfully")
        return result
    logger.warning("No news found for the requested page")
    raise HTTPException(status_code=404, detail="Новости не найдены")


@router.patch("/patch_news/{news_id}", response_model=NewsResponse)
async def patch_news(news_id: int, news_params_to_patch: NewsPatch, current_actor=Depends(get_current_admin)):
    logger.info(f"{current_actor.phone} patches news with ID: {news_id}")
    patched_news = await news_crud.patch_news(news_id=news_id, params=news_params_to_patch)
    if patched_news:
        logger.info(f"News item with ID {news_id} patched successfully")
        return patched_news
    logger.warning(f"News item with ID {news_id} not found for patching")
    raise HTTPException(status_code=404, detail="Новость не найдена")

@router.delete("/delete_news/{news_id}")
async def delete_news(news_id: int, current_actor=Depends(get_current_admin)):
    logger.info(f"{current_actor.phone} deletes news with ID: {news_id}")
    if await news_crud.delete_news(news_id=news_id):
        logger.info(f"News item with ID {news_id} deleted successfully")
        return {"message": "Новость удалена"}
    logger.warning(f"News item with ID {news_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Новость не найдена")