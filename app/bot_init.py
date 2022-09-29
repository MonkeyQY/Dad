import logging
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

api_token = os.getenv('token')
password = os.getenv('password')
telegram_dad = os.getenv('telegram_dad')
telegram_me = os.getenv('telegram_me')
my_email = os.getenv('my_email')

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=api_token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
