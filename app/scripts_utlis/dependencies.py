from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_utils import decode_access_token
from app.crud.user_crud import UserCRUD
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_crud = UserCRUD()

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