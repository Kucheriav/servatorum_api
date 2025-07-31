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
    try:
        payload = decode_access_token(token)
        user_id = payload["user_id"]
        user = await user_crud.get_user(user_id)
        if user is None:
            logger.warning(f"User not found for id {user_id}")
            return None
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired. try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=401, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в get_current_user: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера авторизации")


async def get_current_admin(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        admin_id = payload["admin_id"]
        admin = await admin_crud.get_admin(admin_id)
        if admin is None:
            logger.warning(f"Admin not found for id {admin_id}")
            return None
        return admin
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired. try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=401, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в get_current_user: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера авторизации")


async def user_owner_or_admin(request: Request,  token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        admin_id = payload.get("admin_id")
        if not user_id and not admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token does not contain valid user or admin identifier.")
        if admin_id:
            admin = await admin_crud.get_admin(admin_id)
            if admin is None:
                logger.warning(f"Admin not found for id {admin_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials.")
            return {"role": 'admin', 'current_actor': admin}

        elif user_id:
            user = await user_crud.get_user(user_id)
            if user is None:
                logger.warning(f"User not found for id {user_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials.")
            return {"role": 'user', 'current_actor': user}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown role in the token.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в user_owner_or_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера авторизации")

async def company_owner_or_admin(request: Request, company_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        current_user_id = payload.get("user_id")
        current_admin_id = payload.get("admin_id")
        if not current_user_id and not current_admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token does not contain valid user or admin identifier.")
        if current_admin_id:
            admin = await admin_crud.get_admin(current_admin_id)
            if admin is None:
                logger.warning(f"Admin not found for id {current_admin_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials.")
            return {"role": 'admin', 'current_actor': admin}
        elif current_user_id:
            user_owner = await user_crud.get_user_by_entity(company_id, 'company')
            if user_owner is not None and user_owner.id == current_user_id:
                return {"role": 'user', 'current_actor': user_owner}
            else:
                logger.warning(f"Current user not found as owner for company id {company_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials for company owner.")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown role in the token.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в user_owner_or_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера авторизации")

async def foundation_owner_or_admin(request: Request, foundation_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        current_user_id = payload.get("user_id")
        current_admin_id = payload.get("admin_id")
        if not current_user_id and not current_admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token does not contain valid user or admin identifier.")
        if current_admin_id:
            admin = await admin_crud.get_admin(current_admin_id)
            if admin is None:
                logger.warning(f"Admin not found for id {current_admin_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials.")
            return {"role": 'admin', 'current_actor': admin}
        elif current_user_id:
            user_owner = await user_crud.get_user_by_entity(foundation_id, 'foundation')
            if user_owner is not None and user_owner.id == current_user_id:
                return {"role": 'user', 'current_actor': user_owner}
            else:
                logger.warning(f"Current user not found as owner for foundation id {foundation_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials for foundation owner.")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown role in the token.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в user_owner_or_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера авторизации")

async def fundraising_owner_or_admin(request: Request, fundraising_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        current_user_id = payload.get("user_id")
        current_admin_id = payload.get("admin_id")
        if not current_user_id and not current_admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token does not contain valid user or admin identifier.")
        if current_admin_id:
            admin = await admin_crud.get_admin(current_admin_id)
            if admin is None:
                logger.warning(f"Admin not found for id {current_admin_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials.")
            return {"role": 'admin', 'current_actor': admin}
        elif current_user_id:
            user_owner = await fundraising_crud.get_fundraising_owner(fundraising_id)
            if user_owner is not None and user_owner.id == current_user_id:
                return {"role": 'user', 'current_actor': user_owner}
            else:
                logger.warning(f"Current user not found as owner for fundraising id {fundraising_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid user credentials for fundraising owner.")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown role in the token.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в user_owner_or_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера авторизации")


async def wallet_owner_or_admin(request: Request, wallet_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        current_user_id = payload.get("user_id")
        current_admin_id = payload.get("admin_id")
        if not current_user_id and not current_admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token does not contain valid user or admin identifier.")
        if current_admin_id:
            admin = await admin_crud.get_admin(current_admin_id)
            if admin is None:
                logger.warning(f"Admin not found for id {current_admin_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials.")
            return {"role": 'admin', 'current_actor': admin}
        elif current_user_id:
            user_owner = await wallet_crud.get_user_by_wallet_id(wallet_id)
            if user_owner is not None and user_owner.id == current_user_id:
                return {"role": 'user', 'current_actor': user_owner}
            else:
                logger.warning(f"Current user not found as owner for wallet id {wallet_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Invalid user credentials for wallet owner.")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown role in the token.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в user_owner_or_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера авторизации")



async def transaction_users_or_admin(request: Request, transaction_id: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        current_user_id = payload.get("user_id")
        current_admin_id = payload.get("admin_id")
        if not current_user_id and not current_admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token does not contain valid user or admin identifier.")
        if current_admin_id:
            admin = await admin_crud.get_admin(current_admin_id)
            if admin is None:
                logger.warning(f"Admin not found for id {current_admin_id}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials.")
            return {"role": 'admin', 'current_actor': admin}
        elif current_user_id:
            tx = await transaction_crud.get_transaction(transaction_id)
            allowed_wallet_ids = []
            if tx.sender_wallet_id:
                allowed_wallet_ids.append(tx.sender_wallet_id)
            if tx.recipient_wallet_id:
                allowed_wallet_ids.append(tx.recipient_wallet_id)
            for wallet_id in allowed_wallet_ids:
                try:
                    user = await wallet_crud.get_user_by_wallet_id(wallet_id)
                    if user.id == current_user_id:
                        return {"role": 'user', 'current_actor': user}
                except Exception:
                    continue
            logger.warning(f"Current user not found as owner for wallet id {wallet_id}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid user credentials for wallet owner.")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown role in the token.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token expired. Try to refresh")
    except (jwt.DecodeError, KeyError) as e:
        logger.warning(f"Invalid access token: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный access token")
    except Exception as e:
        logger.error(f"Неизвестная ошибка в user_owner_or_admin: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера авторизации")


async def superadmin_required(current_admin=Depends(get_current_admin)):
    if not getattr(current_admin, "is_superadmin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can perform this action"
        )
    return current_admin