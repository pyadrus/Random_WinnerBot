from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from system.dispatcher import bot, dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"{user_id} {user_name} {user_first_name} {user_last_name} {user_date}")
    sign_up_text = "Добро пожаловать"
    await bot.send_message(message.from_user.id, sign_up_text, disable_web_page_preview=True)


def register_greeting_handler():
    """Регистрируем handlers для бота"""
    dp.message.register(command_start_handler)  # Обработчик команды /start, он же пост приветствия 👋
