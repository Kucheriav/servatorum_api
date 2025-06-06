from datetime import datetime, timedelta
import random
from sqlalchemy.future import select
from app.models.user_model import VerificationCode
from app.models.user_model import User
from app.config import settings
import jwt

CODE_TTL_MINUTES = 5
MAX_ATTEMPTS = 5

from app.database import connection

class AuthCRUD:

    @connection
    async def create_verification_code(self, phone: str, session):
        # Сбросить старые коды для этого телефона
        await session.execute(
            VerificationCode.__table__.update()
            .where(
                VerificationCode.phone == phone,
                VerificationCode.is_used == False
            )
            .values(is_used=True)
        )
        code = f"{random.randint(1000, 9999)}"
        verif_code = VerificationCode(phone=phone, code=code)
        session.add(verif_code)
        await session.commit()
        await session.refresh(verif_code)
        return code

    @connection
    async def verify_code(self, phone: str, code: str, session):
        now = datetime.now()
        stmt = select(VerificationCode).where(
            VerificationCode.phone == phone,
            VerificationCode.is_used is False,
            VerificationCode.created_at >= now - timedelta(minutes=CODE_TTL_MINUTES)
        ).order_by(VerificationCode.created_at.desc())
        result = await session.execute(stmt)
        code_obj = result.scalars().first()
        if not code_obj:
            return "expired"
        if code_obj.attempts >= MAX_ATTEMPTS:
            code_obj.is_used = True
            await session.commit()
            return "locked"
        if code_obj.code != code:
            code_obj.attempts += 1
            await session.commit()
            return "invalid"
        # OK
        code_obj.is_used = True
        await session.commit()
        return "ok"

    @connection
    async def get_or_create_user(self, phone: str, session):
        stmt = select(User).where(User.phone == phone)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if user:
            return user
        user = User(
            login=phone,
            email=f"{phone}@phone.local",
            phone=phone,
            _password="sms_auth"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    def generate_token(self, user: User):
        payload = {"user_id": user.id, "phone": user.phone}
        token = jwt.encode(payload, settings.get_salt(), algorithm="HS256")
        return token