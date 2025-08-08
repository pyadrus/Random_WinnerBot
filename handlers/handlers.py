# -*- coding: utf-8 -*-
import random
import re

from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from system.dispatcher import bot, dp

API_ID = 12345
API_HASH = "0123456789abcdef0123456789abcdef"
SESSION_NAME = "session_name"


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    logger.info(
        f"{message.from_user.id} {message.from_user.username} {message.from_user.first_name} "
        f"{message.from_user.last_name} {message.date.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    await bot.send_message(message.from_user.id, "Пришлите ссылку на пост в Telegram", disable_web_page_preview=True)


async def parse_telegram_link(link: str):
    """
    Разбор ссылки на пост в Telegram.
    Возвращает username/ссылку канала и ID поста.
    """
    # Поддержка форматов:
    # https://t.me/channel/123
    # https://t.me/+invite_link
    pattern = r"(?:https?://)?t\.me/([\w\d_+-]+)/(\d+)"
    match = re.match(pattern, link)
    if match:
        channel_username = match.group(1)
        post_id = int(match.group(2))
        return channel_username, post_id
    return None, None


async def get_random_commenter(channel_username, post_id):
    """Подписка на канал и выбор случайного комментатора"""
    async with TelegramClient(f"setting/account/{SESSION_NAME}", API_ID, API_HASH) as client:
        await client.connect()

        logger.info(f"Подключено к аккаунту Telegram с именем сеанса {SESSION_NAME}")

        # Подписка на канал
        try:
            await client(JoinChannelRequest(channel_username))
            logger.info(f"Подписка на канал {channel_username} выполнена")
        except Exception as e:
            logger.error(f"Ошибка подписки на канал: {e}")

        # Получение комментариев
        commenters = []
        async for msg in client.iter_messages(channel_username, reply_to=post_id, reverse=True):
            sender_id = msg.from_id.user_id if msg.from_id else None
            username = msg.sender.username if msg.sender else None
            if sender_id:
                commenters.append((sender_id, username))
                logger.info(f"Получен комментатор: {sender_id}, @{username}")

        await client.disconnect()

    return random.choice(commenters) if commenters else None


@dp.message()
async def handle_post_link(message: Message):
    """Получаем ссылку, подписываемся на канал и выбираем комментатора"""
    link = message.text.strip()
    channel_username, post_id = await parse_telegram_link(link)

    if not channel_username or not post_id:
        await message.reply("Некорректная ссылка. Пришлите ссылку формата https://t.me/channel/123")
        return

    random_commenter = await get_random_commenter(channel_username, post_id)
    if random_commenter:
        user_id, username = random_commenter
        await message.reply(f"🎉 Победитель: @{username} (ID: {user_id})")
    else:
        await message.reply("Не удалось найти комментаторов.")


def register_greeting_handler():
    """Регистрируем handlers для бота"""
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(handle_post_link)
