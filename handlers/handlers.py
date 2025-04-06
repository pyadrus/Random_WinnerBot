# -*- coding: utf-8 -*-
import json
import random

from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from telethon import TelegramClient

from system.dispatcher import bot, dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    logger.info(f"{message.from_user.id} {message.from_user.username} {message.from_user.first_name} "
                f"{message.from_user.last_name} {message.date.strftime("%Y-%m-%d %H:%M:%S")}")
    await bot.send_message(message.from_user.id, "Добро пожаловать", disable_web_page_preview=True)


# Функция для получения случайного комментатора поста
async def get_random_commenter(channel_id, message_id):
    """Функция для получения случайного комментатора поста"""
    session_name = 'session_name'
    async with TelegramClient(f'setting/account/{session_name}', 12345, '0123456789abcdef0123456789abcdef') as client:
        await client.connect()
        logger.info(f'Подключено к аккаунту Telegram с именем сеанса {session_name}')
        # Список для хранения ID и username пользователей
        commenters = []
        async for message in client.iter_messages(channel_id, reply_to=message_id, reverse=True):
            sender_id = message.from_id.user_id if message.from_id else None
            username = message.sender.username if message.sender else None
            logger.info(
                f"Получен ID пользователя: {sender_id}, Имя пользователя: @{username}")  # Получаем ID пользователя и имя пользователя
            commenters.append((sender_id, username))
        await client.disconnect()  # Отключение от аккаунта Telegram
    return random.choice(commenters)


async def reading_json_file():
    """Чтение JSON файла"""
    with open('config.json', 'r') as file:
        data = json.load(file)
    return data


@dp.message(Command('random_commenter'))
async def random_commenter_handler(message: Message):
    """Обработчик команды /random_commenter"""
    data = await reading_json_file()
    channel_id = data['channel_id']
    post_id = data['post_id']

    random_commenter = await get_random_commenter(channel_id, post_id)
    if random_commenter:
        await message.reply(f"Случайный комментатор: {random_commenter}")
    else:
        await message.reply("Не удалось найти комментаторов.")


def register_greeting_handler():
    """Регистрируем handlers для бота"""
    dp.message.register(command_start_handler)  # Обработчик команды /start, он же пост приветствия 👋
    dp.message.register(random_commenter_handler)  # Обработчик команды /random_comment
