import logging
from fastapi import APIRouter, Response


logger = logging.getLogger("app.sphere_router")
router = APIRouter()

@router.get("/", tags=["root"])
async def root():
    return {"msg": "Servatorum API backend up and running"}

@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    # Можно вернуть пустой ответ или свою favicon
    return Response(status_code=204)

@router.get("/robots.txt", response_class=Response, include_in_schema=False)
async def robots():
    # Обычная заглушка, запрещающая всё для роботов
    content = "User-agent: *\nDisallow: /"
    return Response(content, media_type="text/plain")