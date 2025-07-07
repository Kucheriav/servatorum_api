from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.scripts_utlis.jwt_utils import *
from app.crud.user_crud import UserCRUD
from app.crud.admin_crud import AdminCRUD
from app.models.user_model import User
from app.models.admin_model import Admin
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_crud = UserCRUD()
admin_crud = AdminCRUD()

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    """
    Dependency для защищённых роутов.
    1. Проверяет access_token (JWT), достаёт user.
    2. Если токен просрочен — пытается refresh через refresh_token (из куки).
    3. Если всё неудачно — 401.
    """
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет access token")
    try:
        payload = decode_access_token(token)
        user_id = payload["user_id"]
        user = await user_crud.get_user(user_id)
        return user
    except jwt.ExpiredSignatureError:
        # Попробуем refresh через refresh_token из куки
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token отсутствует, нужна повторная авторизация")
        refreshed = await user_crud.refresh_access_token(refresh_token)
        if refreshed is None:
            raise HTTPException(status_code=401, detail="Refresh token просрочен/невалиден, нужна повторная авторизация")
        # Можно добавить заголовок с новым access_token для фронта
        raise HTTPException(
            status_code=401,
            detail="Access token обновлён, используйте новый токен",
            headers={"X-New-Access-Token": refreshed}
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка проверки токена")

async def get_current_admin(request: Request, token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет access token")
    try:
        payload = decode_access_token(token)
        admin_id = payload["admin_id"]
        admin = await admin_crud.get_admin(admin_id)
        return admin
    except jwt.ExpiredSignatureError:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token отсутствует, нужна повторная авторизация")
        refreshed = await user_crud.refresh_access_token(refresh_token)
        if refreshed is None:
            raise HTTPException(status_code=401, detail="Refresh token просрочен/невалиден, нужна повторная авторизация")
        raise HTTPException(
            status_code=401,
            detail="Access token обновлён, используйте новый токен",
            headers={"X-New-Access-Token": refreshed}
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка проверки токена")

async def owner_or_admin(user_id: int,user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    """
    Dependency для проверки прав: только владелец (user_id) или админ может выполнять действие.
    """
    if admin is not None:
        return {"admin": admin}
    if user is not None and user.id == user_id:
        return {"user": user}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Operation permitted only for owner or admin"
    )

async def superadmin_required(current_admin=Depends(get_current_admin)):
    if not getattr(current_admin, "is_superadmin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can perform this action"
        )
    return current_admin