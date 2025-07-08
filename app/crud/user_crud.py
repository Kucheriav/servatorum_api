from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import connection
from app.models.chat_id_model import *
from app.models.user_model import *
from app.models.sphere_model import *
from app.schemas.user_schema import UserCreate, UserResponse
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


def user_to_schema(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        surname=user.surname,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        city=user.city,
        email=user.email,
        phone=user.phone,
        role=user.role,
        spheres=[s.id for s in user.spheres] if user.spheres else []
    )

class UserCRUD:
    @connection
    async def create_verification_code(self, phone: str, session):
        # Сбросить старые коды для этого телефона
        await session.execute(
            UserVerificationCode.__table__.update()
            .where(
                UserVerificationCode.phone == phone,
                UserVerificationCode.is_used == False
            )
            .values(is_used=True)
        )
        code = f"{random.randint(1000, 9999)}"
        verif_code = UserVerificationCode(phone=phone, code=code)
        session.add(verif_code)
        await session.commit()
        await session.refresh(verif_code)
        return code

    @connection
    async def get_chat_id_for_bot(self, session):
        stmt = select(ChatIdList.chat_id)
        result = await session.execute(stmt)
        chat_ids = result.scalars().all()
        return chat_ids

    @connection
    async def create_new_chat_id_for_bot(self, chat_id: str, session):
        new_chat_id = ChatIdList(chat_id=chat_id)
        session.add(new_chat_id)
        await session.commit()
        await session.refresh(new_chat_id)  # Refresh to get the generated ID
        logger.info(f"Chat_ID created successfully with ID: {new_chat_id.id}")


    @connection
    async def verify_code(self, phone: str, code: str, session):
        # dont work idkn why
        # now = datetime.now()
        # stmt = select(VerificationCode).where(
        #     VerificationCode.phone == phone,
        #     VerificationCode.is_used is False,
        #     VerificationCode.created_at >= now - timedelta(minutes=CODE_TTL_MINUTES)
        # ).order_by(VerificationCode.created_at.desc())
        # result = await session.execute(stmt)
        # code_obj = result.scalars().first()
        now = datetime.now()
        codes_query = select(UserVerificationCode).where(
            UserVerificationCode.phone == phone,
            UserVerificationCode.is_used == False
        ).order_by(UserVerificationCode.created_at.desc())
        result = await session.execute(codes_query)
        codes = result.scalars().all()
        # logging this!
        # logger.info(f"Найдено {len(codes)} неиспользованных кодов для телефона {phone} на {now}")
        # for idx, c in enumerate(codes):
        #     logger.info(
        #         f"[{idx}] code={c.code}, created_at={c.created_at}, attempts={c.attempts} "
        #         f"is_used={c.is_used}, сравниваем с порогом: {now - timedelta(minutes=CODE_TTL_MINUTES)}"
        #     )
        code_obj = None
        for c in codes:
            if c.created_at >= now - timedelta(minutes=CODE_TTL_MINUTES):
                code_obj = c
                break
        if not code_obj:
            raise CodeExpired
        if code_obj.attempts >= MAX_ATTEMPTS:
            code_obj.is_used = True
            await session.commit()
            raise CodeLocked
        if code_obj.code != code:
            code_obj.attempts += 1
            await session.commit()
            raise CodeInvalid
        # OK
        code_obj.is_used = True
        await session.commit()
        user = await self.get_user_by_phone(phone)
        if user:
            access_token = generate_user_access_token(user.id)
            refresh_token_obj = await self.create_refresh_token(user.id)
            result = await session.execute(
                select(User).options(selectinload(User.spheres)).where(User.id == user.id)
            )
            user_with_spheres = result.scalars().first()
            user_schema = user_to_schema(user_with_spheres)
            return {'status': 'ok', 'is_new': False,'user': user_schema, 'access_token': access_token, 'refresh_token': refresh_token_obj.refresh_token}
        else:
            return {'status': 'ok', 'is_new': True}

    @connection
    async def get_user_by_phone(self, phone: str, session):
        stmt = select(User).where(User.phone == phone)
        result = await session.execute(stmt)
        return result.scalars().first()

    @connection
    async def create_refresh_token(self, user_id: int, session):
        refresh_token = generate_refresh_token()
        valid_before = get_refresh_token_expiry()
        user_token = UserToken(access_token=None, refresh_token=refresh_token, valid_before=valid_before, user_id=user_id)
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
        if not token_obj:
            raise NotFoundError('Refresh_token', refresh_token)
        elif token_obj[0].valid_before < datetime.now():
            raise RefreshTokenExpired('RefreshTokenExpired')
        user_id = token_obj[0].user_id
        new_access = generate_user_access_token(user_id)
        return new_access

    @connection
    async def create_user(self, user: UserCreate, session):
        logger.info("Creating a new user")
        try:
            verif_code = await session.execute(
                select(UserVerificationCode)
                .where(
                    UserVerificationCode.phone == user.phone,
                    UserVerificationCode.is_used == True,  # был использован (подтверждён)
                    UserVerificationCode.created_at >= datetime.now() - timedelta(minutes=CODE_TTL_MINUTES)
                )
                .order_by(UserVerificationCode.created_at.desc())
            )
            verif_code = verif_code.scalars().first()
            if not verif_code:
                raise RegistrationError("Телефон не подтверждён или истёк код верификации.")

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
                spheres=sphere_objects
            )
            # new_user.set_password(user.password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Refresh to get the generated ID
            logger.info(f"User created successfully with ID: {new_user.id}")
            access_token = generate_user_access_token(new_user.id)
            refresh_token_obj = await self.create_refresh_token(new_user.id)
            result = await session.execute(
                select(User).options(selectinload(User.spheres)).where(User.id == new_user.id)
            )
            user_with_spheres = result.scalars().first()

            user_schema = user_to_schema(user_with_spheres)
            return {'user': user_schema, 'access_token': access_token, 'refresh_token': refresh_token_obj.refresh_token}
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
    async def get_user_by_entity(self, entity_id: int, entity_type: str, session):
        logger.info(f"Fetching user for entity_id={entity_id}, entity_type='{entity_type}'")
        try:
            # Находим связь пользователь-сущность
            stmt = select(UserEntityRelation).where(
                UserEntityRelation.entity_id == entity_id,
                UserEntityRelation.entity_type == entity_type
            )
            relation_result = await session.execute(stmt)
            relation = relation_result.scalars().first()
            if not relation:
                logger.warning(f"No user relation found for entity_id={entity_id}, entity_type='{entity_type}'")
                raise NotFoundError('UserEntityRelation', f"{entity_type}:{entity_id}")
            user = await session.get(User, relation.user_id)
            if user:
                logger.info(
                    f"User with ID {relation.user_id} retrieved successfully for entity {entity_type}:{entity_id}")
                return user
            else:
                logger.warning(f"User with ID {relation.user_id} not found")
                raise NotFoundError('User', relation.user_id)
        except Exception as e:
            logger.error(
                f"Error occurred while fetching user for entity_id={entity_id}, entity_type='{entity_type}'",
                exc_info=True
            )
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
                        raise UpdateError('User', user_id)
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

