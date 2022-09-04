from aiogram.utils import executor

from app.bot_init import dp
from app.handlers import register_handlers


register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

