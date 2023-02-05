from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#приветственное меню
inline_btn_1 = InlineKeyboardButton('Калькулятор экономии 🧮', callback_data='calculator')
inline_btn_2 = InlineKeyboardButton('Как стать участником? ✅', callback_data='how_to')
inline_btn_3 = InlineKeyboardButton('О проекте ⭐', callback_data='about')
inline_btn_4 = InlineKeyboardButton('🔒Закрытый клуб🔒', callback_data='vip')
inline_btn_5 = InlineKeyboardButton('⚡️Ответы на вопросы⚡️', callback_data='a')
inline_btn_6 = InlineKeyboardButton('Сотрудничество 🤝', callback_data='collaboration')
keyboardHelloMenu = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5, inline_btn_6)

#Главное меню
inline_btn_1 = InlineKeyboardButton('Калькулятор экономии 🧮', callback_data='calculator')
inline_btn_2 = InlineKeyboardButton('Как стать участником? ✅', callback_data='how_to')
inline_btn_3 = InlineKeyboardButton('О проекте ⭐', callback_data='about')
inline_btn_4 = InlineKeyboardButton('🔒Закрытый клуб🔒', callback_data='vip')
inline_btn_5 = InlineKeyboardButton('⚡️Ответы на вопросы⚡️', callback_data='a')
keyboardMainMenu = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)


#Калькулятор
inline_btn_1 = InlineKeyboardButton('НАЧАТЬ 🧮', callback_data='begin')
inline_btn_2 = InlineKeyboardButton('В главное меню ↩', callback_data='back')
keyboardMainCalculator = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

inline_btn_1 = InlineKeyboardButton('Как стать участником? ✅', callback_data='how_to')
inline_btn_2 = InlineKeyboardButton('В главное меню ↩️', callback_data='menu')
keyboardEndCalculator = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)


#how_to
inline_btn_1 = InlineKeyboardButton('Оплатить ✅', callback_data='pay')
inline_btn_2 = InlineKeyboardButton('Узнать подробнее ⚡️', callback_data='more')
inline_btn_3 = InlineKeyboardButton('Назад ↩', callback_data='menu')
keyboardHowTo1 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3)

inline_btn_1 = InlineKeyboardButton('📍Посмотреть список партнёров', callback_data='more')
inline_btn_2 = InlineKeyboardButton('Калькулятор экономии 🧮', callback_data='calculator')
inline_btn_3 = InlineKeyboardButton('Назад ↩', callback_data='back')
keyboardHowTo2 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3)


inline_btn_1 = InlineKeyboardButton('Стать участником ✅', callback_data='pay')
inline_btn_2 = InlineKeyboardButton('Посмотреть подробный файл 📩', callback_data='file')
inline_btn_3 = InlineKeyboardButton('Назад ↩', callback_data='back')
keyboardHowTo3 = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3)


#back
inline_btn_1 = InlineKeyboardButton('Назад ↩', callback_data='menu')
keyboardBack = InlineKeyboardMarkup(row_width=1).add(inline_btn_1)

#оплата
inline_btn_1 = InlineKeyboardButton('Картой 💳', pay=True)
inline_btn_2 = InlineKeyboardButton('В меню ↩', callback_data='main_menu')
keyboardPay = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

#invoice
inline_btn_1 = InlineKeyboardButton('Оплатить', pay=True)
inline_btn_2 = InlineKeyboardButton('В меню ↩', callback_data='main_menu')
keyboardInvoce = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)