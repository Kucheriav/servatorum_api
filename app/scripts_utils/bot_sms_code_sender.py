from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
import logging
from app.config import settings
from app.crud.user_crud import UserCRUD

logger = logging.getLogger("bot")
user_crud = UserCRUD()




bot = Bot(token=settings.get_bot_api())
dp = Dispatcher()

async def start_bot():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Привет! Я рассылаю смс коды. Вперед тестировать авторизацию!")
    logger.info("got message from user")
    chat_id_list = await user_crud.get_chat_id_for_bot()
    if not (message.chat.id in chat_id_list):
        await user_crud.create_new_chat_id_for_bot(message.chat.id)
        await bot.send_message(message.chat.id, 'Вы успешно добавлены в список на рассылку смс-кодов')
    else:
        await bot.send_message(message.chat.id, 'Вы уже добавлены в список на рассылку')

# def start_bot_polling():
#     import threading
#     logger.info("starting polling")
#     threading.Thread(target=bot.polling, daemon=True).start()
#

#
# def start_bot_polling():
#     import threading
#     threading.Thread(target=lambda: executor.start_polling(dp, skip_updates=True), daemon=True).start()