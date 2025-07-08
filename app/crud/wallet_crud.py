from sqlalchemy.future import select
import logging
from app.database import connection
from app.models import Wallet, User
from app.schemas.wallet_schema import WalletCreate, WalletResponse, WalletPatch
from app.errors_custom_types import *

logger = logging.getLogger("app.wallet_crud")
FORBIDDEN_FIELDS = {"id", "created_at", "updated_at"}

class WalletCRUD:
    @connection
    async def create_wallet(self, wallet: WalletCreate, session):
        logger.info(f"Creating wallet for {wallet.owner_type} with id={wallet.owner_id}")
        try:
            new_wallet = Wallet(**wallet.model_dump())
            session.add(new_wallet)
            await session.flush()
            await session.refresh(new_wallet)
            return new_wallet
        except Exception as e:
            logger.error("Error occurred while creating wallet", exc_info=True)
            raise

    @connection
    async def get_wallet(self, wallet_id: int, session):
        logger.info(f"Fetching wallet with ID: {wallet_id}")
        try:
            wallet = await session.get(Wallet, wallet_id)
            if not wallet:
                logger.warning(f"Wallet id={wallet_id} not found")
                raise NotFoundError('Wallet', wallet_id)
            logger.info(f"Wallet with ID {wallet_id} retrieved successfully")
            return wallet
        except Exception as e:
            logger.error(f"Error occurred while fetching wallet with ID {wallet_id}", exc_info=True)
            raise

    @connection
    async def get_wallet_by_owner(self, owner_type: str, owner_id: int, session):
        logger.info(f"Fetching wallet {owner_type} by owner ID: {owner_id}")
        try:
            query = select(Wallet).where(Wallet.owner_type == owner_type, Wallet.owner_id == owner_id)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()
            if not wallet:
                logger.warning(f"Wallet for {owner_type} id={owner_id} not found")
                raise NotFoundError(f"Wallet for {owner_type}", owner_id)
            logger.info(f"Wallet {owner_type} by owner ID {owner_id} retrieved successfully")
            return wallet
        except Exception as e:
            logger.error(f"Error occurred while fetching wallet {owner_type} by owner ID {owner_id}", exc_info=True)
            raise

    @connection
    async def get_user_by_wallet_id(self, wallet_id: int, session):
        wallet = await session.get(Wallet, wallet_id)
        if not wallet:
            raise NotFoundError('Wallet', wallet_id)

        from app.crud.user_crud import UserCRUD
        from app.crud.fundraising_crud import FundraisingCRUD
        user_crud = UserCRUD()
        fundraising_crud = FundraisingCRUD()

        if wallet.owner_type == 'user':
            user = await session.get(User, wallet.owner_id)
            if not user:
                raise NotFoundError('User', wallet.owner_id)
            return user
        elif wallet.owner_type == 'company':
            user = await user_crud.get_user_by_entity(wallet.owner_id, 'company')
            if not user:
                raise NotFoundError('USER_FOR_COMPANY', wallet.owner_id)
            return user
        elif wallet.owner_type == 'foundation':
            user = await user_crud.get_user_by_entity(wallet.owner_id, 'foundation')
            if not user:
                raise NotFoundError('USER_FOR_FOUNDATION', wallet.owner_id)
            return user
        elif wallet.owner_type == 'fundraising':
            user = await fundraising_crud.get_fundraising_owner(wallet.owner_id)
            if not user:
                raise NotFoundError('USER_FOR_FUNDRAISING', wallet.owner_id)
            return user
        else:
            raise NotFoundError('Unknown owner_type', wallet.owner_type)


    @connection
    async def patch_wallet(self, wallet_id: int, session, params):
        logger.info(f"Patching wallet with ID: {wallet_id}")
        try:
            wallet = await session.get(Wallet, wallet_id)
            if not wallet:
                logger.warning(f"Wallet id={wallet_id} not found for patching")
                raise NotFoundError('Wallet', wallet_id)
            for key, value in params.items():
                if key in FORBIDDEN_FIELDS:
                    logger.warning(f"Attempt to patch forbidden field {key} for Wallet ID {wallet_id}")
                    continue
                setattr(wallet, key, value)
            await session.flush()
            await session.refresh(wallet)
            logger.info(f"Wallet with ID {wallet_id} patched successfully")
            return wallet
        except Exception as e:
            logger.error(f"Error occurred while patching wallet with ID {wallet_id}", exc_info=True)
            raise

    @connection
    async def delete_wallet(self, wallet_id: int, session):
        logger.info(f"Deleting wallet with ID: {wallet_id}")
        try:
            wallet = await session.get(Wallet, wallet_id)
            if not wallet:
                logger.warning(f"Wallet with ID {wallet_id} not found")
                raise NotFoundError('Wallet', wallet_id)
            await session.delete(wallet)
            logger.info(f"Wallet with ID {wallet_id} deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error occurred while deleting wallet with ID {wallet_id}", exc_info=True)
            raise
