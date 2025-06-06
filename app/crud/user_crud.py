import logging
from app.database import connection
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.errors_custom_types import *

logger = logging.getLogger("app.user_crud")


class UserCRUD:
    @connection
    async def get_user_by_phone(self, phone: str, session):
        stmt = session.select(User).where(User.phone == phone)
        result = await session.execute(stmt)
        return result.scalars().first()

    @connection
    async def create_user_step1(self, phone, name, profile_picture, session):
        # создать user с минимальными полями
        user = User(login=phone, phone=phone, first_name=name, profile_picture=profile_picture)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @connection
    async def update_user_step2(self, phone, other_fields, session):
        user = await self.get_user_by_phone(phone, session)
        for key, value in other_fields.items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user

    @connection
    async def create_user_minimal(self, phone, session):
        user = User(login=phone, phone=phone)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    @connection
    async def create_user(self, user: UserCreate, session):
        logger.info("Creating a new user")
        try:
            new_user = User(
                login=user.login,
                first_name=user.first_name,
                surname=user.surname,
                last_name=user.last_name,
                date_of_birth=user.date_of_birth,
                gender=user.gender,
                city=user.city,
                address=user.address,
                email=user.email,
                phone=user.phone,
                profile_picture=None
            )
            new_user.set_password(user.password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Refresh to get the generated ID
            logger.info(f"User created successfully with ID: {new_user.id}")
            return new_user

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

