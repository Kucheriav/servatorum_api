from sqlalchemy.future import select
from app.database import connection
from app.models.user_model import *
from app.models.sphere_model import *
from app.schemas.user_schema import UserCreate
from app.errors_custom_types import *
from app.scripts_utlis.token_utils import *
from app.scripts_utlis.jwt_utils import *
from datetime import datetime, timedelta
import random
import logging
import jwt

logger = logging.getLogger("app.user_crud")
CODE_TTL_MINUTES = 5
MAX_ATTEMPTS = 5



class UserCRUD:
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
        # also check if user exist
        now = datetime.now()
        stmt = select(VerificationCode).where(
            VerificationCode.phone == phone,
            VerificationCode.is_used is False,
            VerificationCode.created_at >= now - timedelta(minutes=CODE_TTL_MINUTES)
        ).order_by(VerificationCode.created_at.desc())
        result = await session.execute(stmt)
        code_obj = result.scalars().first()
        if not code_obj:
            return {'status': 'expired'}
        if code_obj.attempts >= MAX_ATTEMPTS:
            code_obj.is_used = True
            await session.commit()
            return {'status': 'locked'}
        if code_obj.code != code:
            code_obj.attempts += 1
            await session.commit()
            return {'status': 'invalid'}
        # OK
        code_obj.is_used = True
        await session.commit()
        user = await self.get_user_by_phone(phone)
        if user:
            access_token = generate_access_token(user.id)
            refresh_token_obj = await self.create_refresh_token(user.id)
            return {'status': 'ok', 'is_new': False,'user': user, 'access_token': access_token, 'refresh_token': refresh_token_obj.refresh_token}
        else:
            return {'status': 'ok', 'is_new': True}

    @connection
    async def get_user_by_phone(self, phone: str, session):
        stmt = session.select(User).where(User.phone == phone)
        result = await session.execute(stmt)
        return result.scalars().first()

    @connection
    async def create_refresh_token(self, user_id: int, session):
        refresh_token = generate_refresh_token()
        valid_before = get_refresh_token_expiry()
        user_token = UserToken(token=None, refresh_token=refresh_token, valid_before=valid_before, user_id=user_id)
        session.add(user_token)
        await session.commit()
        await session.refresh(user_token)
        return user_token

    @connection
    async def refresh_access_token(self, refresh_token: str, session):
        # Ищем refresh_token в таблице
        token_obj = await session.execute(
            UserToken.__table__.select().where(UserToken.refresh_token == refresh_token)
        )
        token_obj = token_obj.first()
        if not token_obj or token_obj[0].valid_before < datetime.now():
            return None
        user_id = token_obj[0].user_id
        # Генерируем новый access_token
        new_access = generate_access_token(user_id)
        return new_access

    @connection
    async def create_user(self, user: UserCreate, session):
        logger.info("Creating a new user")
        try:
            spheres = await session.execute(select(Sphere).where(Sphere.id.in_(user.spheres)))
            sphere_objects = spheres.scalars().all()
            new_user = User(
                first_name=user.first_name,
                surname=user.surname,
                last_name=user.last_name,
                date_of_birth=user.date_of_birth,
                gender=user.gender,
                city=user.city,
                address=user.address,
                email=user.email,
                phone=user.phone,
                profile_picture=None,
                role=user.role,
                spheres=user.spheres
            )
            new_user.set_password(user.password)
            new_user.set_password(user.password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Refresh to get the generated ID
            logger.info(f"User created successfully with ID: {new_user.id}")
            access_token = generate_access_token(user.id)
            refresh_token_obj = await self.create_refresh_token(user.id)
            return {'user': new_user, 'access_token': access_token, 'refresh_token': refresh_token_obj.refresh_token}
        except Exception as e:
            logger.error("Error occurred while creating user", exc_info=True)
            raise

    @connection
    async def get_user(self, user_id: int, session):
        logger.info(f"Fetching user with ID: {user_id}")
        try:
            user = await session.get(User, user_id)
            if user:
                logger.info(f"User with ID {user_id} retrieved successfully")
                return user
            else:
                logger.warning(f"User with ID {user_id} not found")
                raise NotFoundError('User', user_id)
        except Exception as e:
            logger.error(f"Error occurred while fetching user with ID {user_id}", exc_info=True)
            raise

    @connection
    async def patch_user(self, user_id: int, session, params):
        try:
            user_to_patch = await session.get(User, user_id)
            if user_to_patch:
                for key, value in params.params.items():
                    if hasattr(user_to_patch, key):
                        setattr(user_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for user ID {user_id}")
                    else:
                        logger.warning(f"Field {key} not found in User model")
                        raise UserUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                await session.refresh(user_to_patch)
                logger.info(f"User with ID {user_id} patched successfully")
                return user_to_patch
            else:
                logger.warning(f"User with ID {user_id} not found")
                raise NotFoundError('User', user_id)
        except Exception as e:
            logger.error(f"Error occurred while patching user with ID {user_id}", exc_info=True)
            raise


    @connection
    async def delete_user(self, user_id: int, session):
        logger.info(f"Deleting user with ID: {user_id}")
        try:
            user_to_delete = await session.get(User, user_id)
            if user_to_delete:
                await session.delete(user_to_delete)
                await session.commit()
                logger.info(f"User with ID {user_id} deleted successfully")
                return True
            else:
                logger.warning(f"User with ID {user_id} not found")
                raise NotFoundError('User', user_id)
        except Exception as e:
            logger.error(f"Error occurred while deleting user with ID {user_id}", exc_info=True)
            raise

