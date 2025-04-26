from app.database import connection
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.errors_custom_types import *
import logging

# Create a logger specific to this module
logger = logging.getLogger("app.user_crud")


class UserCRUD:
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
                profile_picture=None
            )
            new_user.set_password(user.password)

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Refresh to get the generated ID
            logger.info(f"User created successfully with ID: {new_user.id}")
            return {
                "user_id": new_user.id,
                "login": new_user.login,
                "email": new_user.email,
                "phone": new_user.phone,
                "first_name": new_user.first_name,
                "surname": new_user.surname,
                "last_name": new_user.last_name,
                "date_of_birth": new_user.date_of_birth,
                "gender": new_user.gender,
                "city": new_user.city,
            }
        except Exception as e:
            logger.error("Error occurred while creating user", exc_info=True)
            raise

    @connection
    async def get_user(self, user_id: int, session):
        logger.info(f"Fetching user with ID: {user_id}")
        user = session.select(User).filter(User.id == user_id).first()
        if user:
            logger.info(f"User with ID {user_id} retrieved successfully")
            return user
        else:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")

    @connection
    async def patch_user(self, user_id: int, session, **params):
        logger.info(f"Patching user with ID: {user_id}")
        user_to_patch = session.select(User).filter(User.id == user_id).first()
        if user_to_patch:
            try:
                for key, value in params.items():
                    if hasattr(user_to_patch, key):
                        setattr(user_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for user ID {user_id}")
                    else:
                        logger.warning(f"Field {key} not found in User model")
                        raise UserUpdateError(f"FIELD_NOT_FOUND: {key}")
                await session.commit()
                logger.info(f"User with ID {user_id} patched successfully")
                return user_to_patch
            except Exception as e:
                logger.error("Error occurred while patching user", exc_info=True)
                raise
        else:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")

    @connection
    async def delete_user(self, user_id: int, session):
        logger.info(f"Deleting user with ID: {user_id}")
        user_to_delete = session.select(User).filter(User.id == user_id).first()
        if user_to_delete:
            try:
                session.delete(user_to_delete)
                await session.commit()
                logger.info(f"User with ID {user_id} deleted successfully")
                return True
            except Exception as e:
                logger.error("Error occurred while deleting user", exc_info=True)
                raise
        else:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")