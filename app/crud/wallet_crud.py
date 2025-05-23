from sqlalchemy.future import select
import logging
from datetime import datetime
from app.database import connection
from app.models.user_model import User
from app.models.user_wallet_model  import UserWalletTransaction
from app.errors_custom_types import *

logger = logging.getLogger("app.wallet_crud")


class WalletCRUD:
    @connection
    async def get_balance(self, user_id: int, session):
        logger.info(f"Fetching balance for user ID: {user_id}")
        try:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                logger.info(f"Balance for user ID {user_id}: {user.balance}")
                return user.balance
            else:
                logger.warning(f"User with ID {user_id} not found")
                raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")
        except Exception as e:
            logger.error(f"Error occurred while fetching balance for user ID {user_id}", exc_info=True)
            raise

    @connection
    async def get_history(self, user_id: int, session):
        logger.info(f"Fetching wallet history for user ID: {user_id}")
        try:
            query = select(UserWalletTransaction).where(
                UserWalletTransaction.user_id == user_id
            ).order_by(UserWalletTransaction.created_at.desc())
            result = await session.execute(query)
            history = result.scalars().all()
            logger.info(f"Found {len(history)} transactions for user ID {user_id}")
            return history
        except Exception as e:
            logger.error(f"Error occurred while fetching wallet history for user ID {user_id}", exc_info=True)
            raise

    @connection
    async def deposit(self, user_id: int, amount: float, comment: str, session):
        logger.info(f"Depositing {amount} to user ID: {user_id}")
        try:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                logger.warning(f"User with ID {user_id} not found")
                raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")
            user.balance += amount
            transaction = UserWalletTransaction(
                user_id=user_id,
                type="deposit",
                amount=amount,
                comment=comment,
                created_at=datetime.utcnow()
            )
            session.add(transaction)
            await session.commit()
            await session.refresh(user)
            await session.refresh(transaction)
            logger.info(f"Deposit successful for user ID {user_id}")
            return transaction
        except Exception as e:
            logger.error(f"Error occurred during deposit for user ID {user_id}", exc_info=True)
            raise

    @connection
    async def withdraw(self, user_id: int, amount: float, comment: str, session):
        logger.info(f"Withdrawing {amount} from user ID: {user_id}")
        try:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                logger.warning(f"User with ID {user_id} not found")
                raise UserNotFoundError(f"USER_NOT_FOUND: {user_id}")
            if user.balance < amount:
                logger.warning(f"Insufficient funds for user ID {user_id}: balance {user.balance}, requested {amount}")
                raise InsufficientFundsError(f"INSUFFICIENT_FUNDS: {user_id}")
            user.balance -= amount
            transaction = UserWalletTransaction(
                user_id=user_id,
                type="withdrawal",
                amount=amount,
                comment=comment,
                created_at=datetime.utcnow()
            )
            session.add(transaction)
            await session.commit()
            await session.refresh(user)
            await session.refresh(transaction)
            logger.info(f"Withdrawal successful for user ID {user_id}")
            return transaction
        except InsufficientFundsError as e:
            raise
        except Exception as e:
            logger.error(f"Error occurred during withdrawal for user ID {user_id}", exc_info=True)
            raise