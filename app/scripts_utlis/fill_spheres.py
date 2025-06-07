import asyncio
from app.database import async_session_maker
from sqlalchemy.future import select
from app.models.sphere_model import Sphere

SPHERES = [
    "Доступная среда",
    "Лечение",
    "Безопасная среда",
    # ... и т.д.
]

async def main():
    async with async_session_maker() as session:
        for name in SPHERES:
            exists = await session.execute(
                select(Sphere).where(Sphere.name == name)
            )
            if not exists.scalar_one_or_none():
                session.add(Sphere(name=name))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())