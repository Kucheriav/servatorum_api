from app.database import Database
from app.models.user import User
from app.schemas.user import UserCreate


class UserCRUD:
    def create_user(self, user: UserCreate):
        with Database() as db:
            new_user = User(username=user.username, email=user.email)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    def get_user(self, userid: int):
        with Database() as db:
            return db.query(User).filter(User.id == userid).first()

    def update_user(self, user_id: int, user: UserCreate):
        with Database() as db:
            user_to_update = self.get_user(user_id)
            if user_to_update:
                user_to_update.username = user.username
                user_to_update.email = user.email
                db.commit()
                return user_to_update
            return None

    def delete_user(self, user_id: int):
        with Database() as db:
            user_to_delete = self.get_user(user_id)
            if user_to_delete:
                db.delete(user_to_delete)
                db.commit()
                return True
            return False