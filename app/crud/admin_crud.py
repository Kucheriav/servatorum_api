from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import connection
from app.models.chat_id_model import *
from app.models.admin_model import *
from app.schemas.admin_schema import AdminCreate
from app.errors_custom_types import *
from app.scripts_utils.jwt_utils import *
from datetime import datetime, timedelta
import random
import logging


logger = logging.getLogger("app.admin_crud")
CODE_TTL_MINUTES = 5
MAX_ATTEMPTS = 5
FORBIDDEN_FIELDS = {"id", "created_at", "updated_at"}

class AdminCRUD:
    @connection
    async def create_verification_code(self, phone: str, session):
        # Сбросить старые коды для этого телефона
        await session.execute(
            AdminVerificationCode.__table__.update()
            .where(
                AdminVerificationCode.phone == phone,
                AdminVerificationCode.is_used == False
            )
            .values(is_used=True)
        )
        code = f"{random.randint(1000, 9999)}"
        verif_code = AdminVerificationCode(phone=phone, code=code)
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
        # don't work idkn why
        # now = datetime.now()
        # stmt = select(VerificationCode).where(
        #     VerificationCode.phone == phone,
        #     VerificationCode.is_used is False,
        #     VerificationCode.created_at >= now - timedelta(minutes=CODE_TTL_MINUTES)
        # ).order_by(VerificationCode.created_at.desc())
        # result = await session.execute(stmt)
        # code_obj = result.scalars().first()
        now = datetime.now()
        codes_query = select(AdminVerificationCode).where(
            AdminVerificationCode.phone == phone,
            AdminVerificationCode.is_used == False
        ).order_by(AdminVerificationCode.created_at.desc())
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
        admin = await self.get_admin_by_phone(phone)
        if admin:
            access_token = generate_admin_access_token(admin.id, admin.is_superadmin)
            refresh_token_obj = await self.create_refresh_token(admin.id)
            return {'status': 'ok', 'is_new': False,'admin': admin, 'access_token': access_token, 'refresh_token': refresh_token_obj.refresh_token}
        else:
            return {'status': 'ok', 'is_new': True}

    @connection
    async def get_admin_by_phone(self, phone: str, session):
        stmt = select(Admin).where(Admin.phone == phone)
        result = await session.execute(stmt)
        return result.scalars().first()

    @connection
    async def create_refresh_token(self, admin_id: int, session):
        refresh_token = generate_refresh_token()
        valid_before = get_refresh_token_expiry()
        admin_token = AdminToken(token=None, refresh_token=refresh_token, valid_before=valid_before, user_id=admin_id)
        session.add(admin_token)
        await session.commit()
        await session.refresh(admin_token)
        return admin_token

    @connection
    async def refresh_access_token(self, refresh_token: str, session):
        token_obj = await session.execute(
            AdminToken.__table__.select().where(AdminToken.refresh_token == refresh_token)
        )
        token_obj = token_obj.first()
        if not token_obj:
            raise NotFoundError('Refresh_token', refresh_token)
        elif token_obj[0].valid_before < datetime.now():
            raise RefreshTokenExpired('RefreshTokenExpired')
        admin = session.get(Admin, token_obj[0].admin_id)
        new_access = generate_admin_access_token(admin.id, admin.is_superadmin)
        return new_access

    @connection
    async def create_admin(self, admin: AdminCreate, session):
        logger.info("Creating a new admin")
        try:
            verif_code = await session.execute(
                select(AdminVerificationCode)
                .where(
                    AdminVerificationCode.phone == admin.phone,
                    AdminVerificationCode.is_used == True,  # был использован (подтверждён)
                    AdminVerificationCode.created_at >= datetime.now() - timedelta(minutes=CODE_TTL_MINUTES)
                )
                .order_by(AdminVerificationCode.created_at.desc())
            )
            verif_code = verif_code.scalars().first()
            if not verif_code:
                raise RegistrationError("Телефон не подтверждён или истёк код верификации.")

            new_admin = Admin(
                username=admin.username,
                email=admin.email,
                phone=admin.phone,
                is_superadmin=admin.is_superadmin,
                profile_picture=None,
            )
            new_admin.set_password(admin.password)
            session.add(new_admin)
            await session.commit()
            await session.refresh(new_admin)  # Refresh to get the generated ID
            logger.info(f"Admin created successfully with ID: {new_admin.id}")
            access_token = generate_admin_access_token(new_admin.id, new_admin.is_superadmin)
            refresh_token_obj = await self.create_refresh_token(new_admin.id)
            return {'admin': new_admin, 'access_token': access_token, 'refresh_token': refresh_token_obj.refresh_token}
        except Exception as e:
            logger.error("Error occurred while creating admin", exc_info=True)
            raise

    @connection
    async def get_admin(self, admin_id: int, session):
        logger.info(f"Fetching user with ID: {admin_id}")
        try:
            admin = await session.get(Admin, admin_id)
            if admin:
                logger.info(f"Admin with ID {admin_id} retrieved successfully")
                return admin
            else:
                logger.warning(f"Admin with ID {admin_id} not found")
                raise NotFoundError('Admin', admin_id)
        except Exception as e:
            logger.error(f"Error occurred while fetching admin with ID {admin_id}", exc_info=True)
            raise

    @connection
    async def patch_admin(self, admin_id: int, session, params):
        try:
            admin_to_patch = await session.get(Admin, admin_id)
            if admin_to_patch:
                for key, value in params.params.items():
                    if hasattr(admin_to_patch, key):
                        if key in FORBIDDEN_FIELDS:
                            logger.warning(f"Attempt to patch forbidden field {key} for Admin ID {admin_id}")
                            continue
                        setattr(admin_to_patch, key, value)
                        logger.debug(f"Updated field {key} to {value} for admin ID {admin_id}")
                    else:
                        logger.warning(f"Field {key} not found in Admin model")
                        raise UpdateError('Admin', admin_id)
                await session.commit()
                await session.refresh(admin_to_patch)
                logger.info(f"Admin with ID {admin_id} patched successfully")
                return admin_to_patch
            else:
                logger.warning(f"Admin with ID {admin_id} not found")
                raise NotFoundError('Admin', admin_id)
        except Exception as e:
            logger.error(f"Error occurred while patching admin with ID {admin_id}", exc_info=True)
            raise


    @connection
    async def delete_admin(self, admin_id: int, session):
        logger.info(f"Deleting user with ID: {admin_id}")
        try:
            admin_to_delete = await session.get(Admin, admin_id)
            if admin_to_delete:
                await session.delete(admin_to_delete)
                await session.commit()
                logger.info(f"Admin with ID {admin_id} deleted successfully")
                return True
            else:
                logger.warning(f"Admin with ID {admin_id} not found")
                raise NotFoundError('Admin', admin_id)
        except Exception as e:
            logger.error(f"Error occurred while deleting admin with ID {admin_id}", exc_info=True)
            raise

