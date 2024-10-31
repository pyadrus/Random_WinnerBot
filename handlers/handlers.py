from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from telethon import TelegramClient

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


# Функция для получения случайного комментатора поста
async def get_random_commenter(channel_id, message_id):
    api_id = 12345
    api_hash = '0123456789abcdef0123456789abcdef'
    session_name = 'session_name'

    async with TelegramClient(f'setting/account/{session_name}', api_id, api_hash) as client:
        await client.connect()
        logger.info(f'Подключено к аккаунту Telegram с именем сеанса {session_name}')

        # Список для хранения ID и username пользователей
        commenters = []

        async for message in client.iter_messages(channel_id, reply_to=message_id, reverse=True):
            sender_id = message.from_id.user_id if message.from_id else None
            username = message.sender.username if message.sender else None
            logger.info(sender_id, username)  # Получаем ID пользователя и имя пользователя
            commenters.append((sender_id, username))

        import random
        random_commenter = random.choice(commenters)

        await client.disconnect()  # Отключение от аккаунта Telegram
    return random_commenter


@dp.message(Command('random_commenter'))
async def random_commenter_handler(message: Message):
    channel_id = '@master_tg_d'  # ID вашего канала или группы
    post_id = 454  # ID поста, к которому нужно получить комментаторов

    random_commenter = await get_random_commenter(channel_id, post_id)

    if random_commenter:
        await message.reply(f"Случайный комментатор: {random_commenter}")
    else:
        await message.reply("Не удалось найти комментаторов.")


def register_greeting_handler():
    """Регистрируем handlers для бота"""
    dp.message.register(command_start_handler)  # Обработчик команды /start, он же пост приветствия 👋
    dp.message.register(random_commenter_handler)  # Обработчик команды /random_comment
