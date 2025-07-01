import telebot
import logging

from telebot.types import Message

from app.config import settings
from app.crud.user_crud import UserCRUD

logger = logging.getLogger("bot")
user_crud = UserCRUD()
bot = telebot.TeleBot(settings.get_bot_api())

@bot.message_handler(content_types=['text'])
def check_user_list(message: Message):
    logger.info("got message from user")
    chat_id_list = user_crud.get_chat_id_for_bot()
    if not (message.chat.id in chat_id_list):
        user_crud.create_new_chat_id_for_bot(message.chat.id)
        bot.send_message(message.chat.id, 'Вы успешно добавлены в список на рассылку смс-кодов')
    else:
        bot.send_message(message.chat.id, 'Вы ужке добавлены в список на рассылку')


def start_bot_polling():
    import threading
    logger.info("starting polling")
    threading.Thread(target=bot.polling, daemon=True).start()