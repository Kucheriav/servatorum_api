from sqlalchemy.future import select
import logging
from app.database import connection
from app.models.sphere_model import Sphere
from app.schemas.sphere_schema import SphereCreate, SpherePatch
from app.errors_custom_types import NotFoundError
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("app.sphere_crud")
FORBIDDEN_FIELDS = {"id", "created_at", "updated_at"}

class SphereCRUD:
    @connection
    async def create_sphere(self, sphere: SphereCreate, session):
        logger.info(f"Creating sphere with name={sphere.name}")
        try:
            new_sphere = Sphere(name=sphere.name)
            session.add(new_sphere)
            await session.flush()
            await session.refresh(new_sphere)
            return new_sphere
        except IntegrityError:
            logger.warning(f"Sphere with name={sphere.name} already exists")
            raise
        except Exception as e:
            logger.error("Unexpected error while creating sphere", exc_info=True)
            raise

    @connection
    async def get_sphere(self, sphere_id: int, session):
        sphere = await session.get(Sphere, sphere_id)
        if not sphere:
            logger.warning(f"Sphere id={sphere_id} not found")
            raise NotFoundError("Сфера", sphere_id)
        return sphere

    @connection
    async def get_all_spheres(self, session):
        result = await session.execute(select(Sphere))
        return result.scalars().all()

    @connection
    async def patch_sphere(self, sphere_id: int, session, patch: SpherePatch):
        sphere = await session.get(Sphere, sphere_id)
        if not sphere:
            logger.warning(f"Sphere id={sphere_id} not found for patch")
            raise NotFoundError("Сфера", sphere_id)
        for key, value in patch.model_dump(exclude_unset=True).items():
            if key in FORBIDDEN_FIELDS:
                logger.warning(f"Attempt to patch forbidden field {key} for Sphere ID {sphere_id}")
                continue
            setattr(sphere, key, value)
        await session.commit()
        await session.refresh(sphere)
        logger.info(f"Sphere id={sphere_id} patched")
        return sphere

    @connection
    async def delete_sphere(self, sphere_id: int, session):
        sphere = await session.get(Sphere, sphere_id)
        if not sphere:
            logger.warning(f"Sphere id={sphere_id} not found for delete")
            raise NotFoundError("Сфера", sphere_id)
        await session.delete(sphere)
        await session.commit()
        logger.info(f"Sphere id={sphere_id} deleted")
        return True