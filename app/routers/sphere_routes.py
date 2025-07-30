from fastapi import APIRouter, HTTPException, Depends

from app.models import Admin
from app.schemas.sphere_schema import SphereCreate, SphereResponse, SpherePatch
from app.crud.sphere_crud import SphereCRUD
from sqlalchemy.exc import IntegrityError
from app.errors_custom_types import NotFoundError
from app.scripts_utils.dependencies import get_current_admin
import logging

router = APIRouter()
crud = SphereCRUD()
logger = logging.getLogger("app.sphere_router")

@router.post("/spheres", response_model=SphereResponse)
async def create_sphere(sphere: SphereCreate, current_admin: Admin=Depends(get_current_admin)):
    logger.info(f"{current_admin.username} creates a sphere")
    try:
        created = await crud.create_sphere(sphere)
        return created
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Сфера с таким именем уже существует")
    except Exception as e:
        logger.error("Ошибка при создании сферы", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/spheres", response_model=list[SphereResponse])
async def get_all_spheres():
    try:
        return await crud.get_all_spheres()
    except Exception as e:
        logger.error("Ошибка при получении списка сфер", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/spheres/{sphere_id}", response_model=SphereResponse)
async def get_sphere(sphere_id: int):
    try:
        return await crud.get_sphere(sphere_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Сфера не найдена")
    except Exception as e:
        logger.error("Ошибка при получении сферы", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/spheres/{sphere_id}", response_model=SphereResponse)
async def patch_sphere(sphere_id: int, patch_data: SpherePatch, current_admin: Admin=Depends(get_current_admin)):
    logger.info(f"{current_admin.username} patches a sphere")
    try:
        return await crud.patch_sphere(sphere_id, patch_data)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Сфера не найдена")
    except Exception as e:
        logger.error("Ошибка при обновлении сферы", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/spheres/{sphere_id}")
async def delete_sphere(sphere_id: int, current_admin: Admin=Depends(get_current_admin)):
    logger.info(f"{current_admin.username} deletes a sphere")
    try:
        await crud.delete_sphere(sphere_id)
        return {"success": True}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Сфера не найдена")
    except Exception as e:
        logger.error("Ошибка при удалении сферы", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")