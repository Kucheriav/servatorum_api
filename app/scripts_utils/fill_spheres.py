import asyncio
from app.database import async_session_maker
from sqlalchemy.future import select
from app.models.sphere_model import Sphere

SPHERES = [
    "Доступная среда",
    "Лечение",
    "Безопасная среда",
    "Психология и психотерапия",
    "Гуманитарная помощь",
    "Социальная поддержка",
    "Наука и искусство",
    "Искусство",
    "Pro-bono",
    "ESG",
    "Профилактика и физиотерапия",
    "Религиозные организации",
    "Волонтеры",
    "Паллиативная помощь",
    "Поисковый отряд",
    "Сообщество волонтеров",
    "Мероприятия фондов"
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