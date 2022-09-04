from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_menu():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(InlineKeyboardButton(text='Изменить Маршрут', callback_data='change_route'))
    keyboard.row(InlineKeyboardButton(text='Вписать почту для отправки', callback_data='mail_to_send'))
    keyboard.row(InlineKeyboardButton(text='Отправить письмо', callback_data='send_file'))
    return keyboard