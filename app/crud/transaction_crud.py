from sqlalchemy.future import select
import logging
from app.database import connection
from app.models import Transaction, User
from app.models.wallet_model import Wallet
from app.schemas.transaction_schema import TransactionCreate
from app.errors_custom_types import *

logger = logging.getLogger("app.transaction_crud")

class TransactionCRUD:
    @connection
    async def create_transaction(self, tx: TransactionCreate, session):
        logger.info(f"Creating transaction type={tx.type} amount={tx.amount}")
        # Валидация на уровне бизнес-логики
        # Проверки наличия кошельков, положительности суммы и т.д.
        sender_wallet = None
        recipient_wallet = None
        if tx.sender_wallet_id:
            sender_wallet = await session.get(Wallet, tx.sender_wallet_id)
            if not sender_wallet:
                logger.warning(f"Sender wallet id={tx.sender_wallet_id} not found")
                raise NotFoundError("Кошелек отправителя не найден")
        if tx.recipient_wallet_id:
            recipient_wallet = await session.get(Wallet, tx.recipient_wallet_id)
            if not recipient_wallet:
                logger.warning(f"Recipient wallet id={tx.recipient_wallet_id} not found")
                raise NotFoundError("Кошелек получателя не найден")
        # (Далее обработка списания/зачисления баланса по логике)
        new_tx = Transaction(**tx.model_dump())
        session.add(new_tx)
        await session.flush()
        await session.refresh(new_tx)
        return new_tx

    @connection
    async def get_transaction(self, transaction_id: int, session):
        tx = await session.get(Transaction, transaction_id)
        if not tx:
            logger.warning(f"Transaction id={transaction_id} not found")
            raise NotFoundError("Транзакция не найдена")
        return tx

    @connection
    async def get_transaction_sender(self, transaction_id: int, session):
        tx = await session.get(Transaction, transaction_id)
        if not tx:
            logger.warning(f"Transaction id={transaction_id} not found")
            raise NotFoundError("Транзакция не найдена")
        return tx


    @connection
    async def get_transactions_for_wallet(self, wallet_id: int, session, limit=30, offset=0):
        stmt = select(Transaction).where(
            (Transaction.sender_wallet_id == wallet_id) | (Transaction.recipient_wallet_id == wallet_id)
        ).order_by(Transaction.created_at.desc()).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.scalars().all()

    @connection
    async def delete_transaction(self, transaction_id: int, session):
        tx = await session.get(Transaction, transaction_id)
        if not tx:
            logger.warning(f"Transaction id={transaction_id} not found for deleting")
            raise NotFoundError("Транзакция не найдена")
        await session.delete(tx)
        return {"message": "Transaction deleted"}
