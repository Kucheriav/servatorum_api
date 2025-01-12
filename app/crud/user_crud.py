from app.database import connection
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.errors_custom_types import *


class UserCRUD:
    @connection
    async def create_user(self, user: UserCreate, session):
        new_user = User(
            login=user.login,
            first_name=user.first_name,
            surname=user.surname,
            last_name=user.last_name,
            date_of_birth=user.date_of_birth,
            gender=user.gender,
            city=user.city,
            profile_picture=None  # Или любое другое значение по умолчанию
        )
        new_user.set_password(user.password)

        session.add(new_user)
        session.commit()
        return new_user

    @connection
    async def get_user(self, user_id: int, session):
        user = session.select(User).filter(User.id == user_id).first()
        if user:
            return user
        else:
            raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")

    @connection
    async def patch_user(self, user_id: int, session, **params):
        user_to_patch = session.select(User).filter(User.id == user_id).first()
        if user_to_patch:
            for key, value in params.items():
                if hasattr(user_to_patch, key):
                    setattr(user_to_patch, key, value)
                else:
                    raise UserUpdateError(f"FIELD_NOT_FOUND: {key}")
            session.commit()
            return user_to_patch
        else:
            raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")

    @connection
    def delete_user(self, user_id: int, session):
        user_to_delete = session.select(User).filter(User.id == user_id).first()
        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            return True
        else:
            raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")