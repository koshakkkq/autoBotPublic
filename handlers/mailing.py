from create import dp
from handlers.hello import back_to_menu_call, stage1_calculator
from aiogram import types, Dispatcher
def register_handlers_client(dp: Dispatcher):


    # calculator
    dp.register_callback_query_handler(back_to_menu_call, state='*', text_startswith='mailing_menu')
    dp.register_callback_query_handler(stage1_calculator, state='*', text_startswith='mailing_calculator')

    #todo добавить номера
    #dp.register_callback_query_handler(back_to_menu_call, state='*', text_startswith='mailing_get_phone')
    #dp.register_callback_query_handler(stage1_calculator, state='*', text_startswith='mailing_pay')
    #dp.register_callback_query_handler(stage1_calculator, state='*', text_startswith='mailing_menu')




