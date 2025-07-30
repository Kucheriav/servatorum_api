from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.scripts_utils.jwt_utils import *
from app.crud.user_crud import UserCRUD
from app.crud.admin_crud import AdminCRUD
from app.crud.fundraising_crud import FundraisingCRUD
from app.crud.wallet_crud import WalletCRUD
from app.crud.transaction_crud import TransactionCRUD
from app.models.user_model import User
from app.models.admin_model import Admin
import jwt
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_crud = UserCRUD()
admin_crud = AdminCRUD()
wallet_crud = WalletCRUD()
fundraising_crud = FundraisingCRUD()
transaction_crud = TransactionCRUD()
logger = logging.getLogger("app.dependencies")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет access token")
    try:
        payload = decode_access_token(token)
        user_id = payload["user_id"]
        user = await user_crud.get_user(user_id)
        return user
    except jwt.ExpiredSignatureError:
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
    except Exception as e:
        return None

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
        return None

async def user_owner_or_admin(user_id: int,user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    if admin is not None:
        logger.info('admin')
        return {"admin": admin}
    if user is not None and user.id == user_id:
        logger.info(f"user: {user.surname}")
        return {"user": user}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Operation permitted only for owner or admin"
    )

async def company_owner_or_admin(company_id: int, current_user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    if admin is not None:
        return {"admin": admin}
    user = await user_crud.get_user_by_entity(company_id, 'company')
    if user is not None and user.id == current_user.id:
        return {"user": user}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Operation permitted only for owner or admin"
    )

async def foundation_owner_or_admin(foundation_id: int, current_user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    if admin is not None:
        return {"admin": admin}
    user = await user_crud.get_user_by_entity(foundation_id, 'foundation')
    if user is not None and user.id == current_user.id:
        return {"user": user}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Operation permitted only for owner or admin"
    )

async def fundraising_owner_or_admin(fundraising_id: int, current_user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    if admin is not None:
        return {"admin": admin}
    user = await fundraising_crud.get_fundraising_owner(fundraising_id)
    if user is not None and user.id == current_user.id:
        return {"user": user}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Operation permitted only for owner or admin"
    )

async def wallet_owner_or_admin(wallet_id: int, current_user=Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    if admin is not None:
        return {"admin": admin}
    user = await wallet_crud.get_user_by_wallet_id(wallet_id)
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому кошельку")
    return {"user": user}


async def transaction_users_or_admin(transaction_id: int, current_user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin)):
    if admin is not None:
        return {"admin": admin}
    tx = await transaction_crud.get_transaction(transaction_id)
    allowed_wallet_ids = []
    if tx.sender_wallet_id:
        allowed_wallet_ids.append(tx.sender_wallet_id)
    if tx.recipient_wallet_id:
        allowed_wallet_ids.append(tx.recipient_wallet_id)
    for wallet_id in allowed_wallet_ids:
        try:
            user = await wallet_crud.get_user_by_wallet_id(wallet_id)
            if user.id == current_user.id:
                return {"user": user}
        except HTTPException:
            continue
    raise HTTPException(status_code=403, detail="Нет доступа к этой транзакции")


# def make_owner_or_admin_dependency(get_obj_by_id, owner_id_attr: str, param_name: str):
#     async def dep(user: User = Depends(get_current_user), admin: Admin = Depends(get_current_admin), **kwargs):
#         obj_id = kwargs.get(param_name, None)
#         obj = await get_obj_by_id(obj_id)
#         if obj is None:
#             raise HTTPException(status_code=404, detail="Object not found")
#         if admin is not None:
#             return {"admin": admin}
#         if user is not None and getattr(obj, owner_id_attr) == user.id:
#             return {"user": user}
#         raise HTTPException(status_code=403, detail="Not allowed")
#     return dep
#
# company_owner_or_admin = make_owner_or_admin_dependency(company_crud.get_company, "owner_id", "company_id")


async def superadmin_required(current_admin=Depends(get_current_admin)):
    if not getattr(current_admin, "is_superadmin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can perform this action"
        )
    return current_admin