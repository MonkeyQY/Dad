from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from app.bot_init import bot, telegram_dad, telegram_me
from app.get_file_and_mail import get_file_and_mail
from app.keyboard_for_bot import keyboard_menu
from app.messages import successes_send, error_send
from app.methods_change_file import get_file
from app.send_file_on_mail import send_email

telegram_id = [int(telegram_me), int(telegram_dad)]


class FSMChange(StatesGroup):
    home_menu = State()
    start_point = State()
    end_point = State()
    get_date = State()
    get_mail = State()


async def start(message: Message):
    if message.chat.id in telegram_id:
        await message.answer('Измени файл, впиши почту  и нажми отправить\n', reply_markup=keyboard_menu())
        await FSMChange.home_menu.set()


async def start_change_file(call: CallbackQuery):
    await call.message.edit_text('Введи город Откуда едешь')
    await FSMChange.start_point.set()


async def get_start_point(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['start_point'] = message.text.strip()
    await bot.send_message(message.chat.id, 'Введи город Куда едешь')
    await FSMChange.end_point.set()


async def get_end_point(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['end_point'] = message.text.strip()
    await bot.send_message(message.chat.id,
                           'Введи дату открытия путевого листа - формата день.месяц.год\n'
                           '26.08.2022')
    await FSMChange.get_date.set()


async def get_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        start_point = data.get('start_point')
        end_point = data.get('end_point')
        doc = await get_file(starting_point=start_point, end_point=end_point, date=message.text.strip())
        await bot.send_document(message.chat.id, ('Файл_ворд.docx', doc.getbuffer()))
        data['file'] = doc
    await FSMChange.home_menu.set()
    await start(message)


async def select_mail(call: CallbackQuery, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Введи почту  или скопируй')
    await FSMChange.get_mail.set()


async def get_mail(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['mail'] = message.text.strip()
    await bot.send_message(message.chat.id, 'Получил email, можешь отправлять файл заказчику')
    await start(message)
    await FSMChange.home_menu.set()


async def send_file(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text('Подожди, отправляю письмо')
    chat_id = call.message.chat.id
    file, mail = await get_file_and_mail()
    list_test = [file, mail]
    match list_test:
        case list_test if None in list_test:
            await not_all_data_has_been_entered(chat_id, msg, call)
        case _:
            await successes_job(chat_id, mail, file, call, msg, state)


async def not_all_data_has_been_entered(chat_id, msg, call):
    await bot.delete_message(chat_id, message_id=msg.message_id)
    await bot.send_message(call.message.chat.id, 'Не все данные были введены')


async def successes_job(chat_id, mail, file, call, msg, state):
    await bot.send_message(chat_id, successes_send.format(mail=mail)) \
        if send_email(file, mail) else await bot.send_message(
        chat_id, error_send)
    await bot.delete_message(chat_id, message_id=msg.message_id)
    await state.finish()
    await start(message=call.message)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_callback_query_handler(start_change_file, text='change_route', state=FSMChange.home_menu)
    dp.register_message_handler(get_start_point, content_types='text', state=FSMChange.start_point)
    dp.register_message_handler(get_end_point, content_types='text', state=FSMChange.end_point)
    dp.register_message_handler(get_date, content_types='text', state=FSMChange.get_date)
    dp.register_callback_query_handler(select_mail, text='mail_to_send', state=FSMChange.home_menu)
    dp.register_message_handler(get_mail, content_types='text', state=FSMChange.get_mail)
    dp.register_callback_query_handler(send_file, text='send_file', state=FSMChange.home_menu)
