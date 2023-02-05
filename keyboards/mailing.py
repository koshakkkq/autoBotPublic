from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#приветственное меню
inline_btn_1 = InlineKeyboardButton('Стать участником ✅', callback_data='mailing_pay')
inline_btn_2 = InlineKeyboardButton('В главное меню ↩', callback_data='mailing_menu')
keyboardHelloMailing = InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

#readThis
inline_btn_1 = InlineKeyboardButton('Да, готов ✅', callback_data='mailing_pay')
inline_btn_2 = InlineKeyboardButton('⚡️У меня остались вопросы⚡️', callback_data='mailing_get_phone')
keyboardReadThis= InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

#toVip
inline_btn_1 = InlineKeyboardButton('Оплатить ✅', callback_data='mailing_pay')
keyboardToVip= InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

#endVip1
inline_btn_1 = InlineKeyboardButton('Стать участником ✅', callback_data='mailing_pay')
inline_btn_2 = InlineKeyboardButton('Калькулятор экономии 🧮', callback_data='mailing_calculator')
inline_btn_3 = InlineKeyboardButton('В главное меню ↩️', callback_data='mailing_menu')
keyboardendVip1= InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3)

inline_btn_1 = InlineKeyboardButton('Стать участником ✅', callback_data='mailing_pay')
inline_btn_2 = InlineKeyboardButton('Связаться с администратором🆘', callback_data='mailing_admin')
inline_btn_3 = InlineKeyboardButton('В главное меню ↩️', callback_data='mailing_menu')
keyboardendVip2= InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2, inline_btn_3)


boards = {'keyboardToVip':keyboardToVip, 'keyboardReadThis':keyboardReadThis, 'keyboardHelloMailing': keyboardHelloMailing,
          'keyboardVipEnd1':keyboardendVip1, 'keyboardVipEnd2':keyboardendVip2}