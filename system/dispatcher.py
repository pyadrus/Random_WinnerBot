# -*- coding: utf-8 -*-
import configparser

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
config.read("setting/config.ini")  # Чтение файла
BOT_TOKEN = config["BOT_TOKEN"]["BOT_TOKEN"]

bot = Bot(
    token=BOT_TOKEN,
)

storage = MemoryStorage()  # Хранилище
dp = Dispatcher(storage=storage)

ADMIN_USER_ID = 535185511

router = Router()
dp.include_router(router)
