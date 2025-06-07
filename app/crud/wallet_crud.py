from sqlalchemy.future import select
import logging
from app.database import connection
from app.models.wallet_model import Wallet
from app.schemas.wallet_schema import WalletCreate, WalletResponse, WalletPatch
from app.errors_custom_types import *

logger = logging.getLogger("app.wallet_crud")

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
    async def patch_wallet(self, wallet_id: int, session, params):
        logger.info(f"Patching wallet with ID: {wallet_id}")
        try:
            wallet = await session.get(Wallet, wallet_id)
            if not wallet:
                logger.warning(f"Wallet id={wallet_id} not found for patching")
                raise NotFoundError('Wallet', wallet_id)
            for key, value in params.items():
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
