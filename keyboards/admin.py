from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import category


#главное меню
inline_btn_1 = InlineKeyboardButton('ВАШ ЛИЧНЫЙ КАБИНЕТ 👨🏼‍💻', callback_data='account')
keyboardMenu = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_btn_2 = InlineKeyboardButton('Продлить подписку ✅', callback_data='pay')
inline_btn_3 = InlineKeyboardButton('📍Список партнёров + админ', callback_data='partners')
keyboardMenu.add(inline_btn_2, inline_btn_3)
inline_btn_4 = InlineKeyboardButton('НАШ КАНАЛ 💭', url='yandex.ru')
inline_btn_5 = InlineKeyboardButton('⚡️ОНЛАЙН ПОМОЩЬ⚡️', callback_data='search_partners')
keyboardMenu.add(inline_btn_4, inline_btn_5)
inline_btn_5 = InlineKeyboardButton('Рассылка vip',callback_data='send_to_vip')
inline_btn_6 = InlineKeyboardButton('Рассылка без vip', callback_data='send_to_default')
keyboardMenu.add(inline_btn_5, inline_btn_6)


#Назад
inline_btn_1 = InlineKeyboardButton('Назад', callback_data='back')
keyboardBack = InlineKeyboardMarkup(row_width=1).add(inline_btn_1)



#назад с удалением
inline_btn_1 = InlineKeyboardButton('Назад', callback_data='back')
inline_btn_2 = InlineKeyboardButton('Удалить❌', callback_data='delete')
keyboardBackDel = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

keyBack = {True:keyboardBackDel, False: keyboardBack}