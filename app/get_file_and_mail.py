from aiogram import Dispatcher


async def get_file_and_mail():
    state = Dispatcher.get_current().current_state()
    async with state.proxy() as data:
        file = data.get('file')
        mail = data.get('mail')
    return file, mail