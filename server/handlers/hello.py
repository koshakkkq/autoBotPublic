from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create import dp
from utils.checkers import is_float
import keyboards
import math


# Менюшки -----

async def reload(message: types.Message, state):
    photo = types.InputFile('pictures/hello.jpg')
    await message.answer_photo(photo=photo,
                               caption=f'Добрый день {message.chat.first_name} 😌 \nДобро пожаловать в "АВТО ТЕМА" \n\nНиже есть интерактивное меню, которое ответит на все ваши вопросы 👇🏼',
                               reply_markup=keyboards.hello.keyboardHelloMenu)
    await state.finish()
    await state.set_state(mainState.state.state)


async def hello_handler(message: types.Message, state):
    photo = types.InputFile('pictures/hello.jpg')
    await message.answer_photo(photo=photo,
                               caption=f'Добрый день {message.chat.first_name} 😌 \nДобро пожаловать в "АВТО ТЕМА" \n\nНиже есть интерактивное меню, которое ответит на все ваши вопросы 👇🏼',
                               reply_markup=keyboards.hello.keyboardHelloMenu)
    await state.finish()
    await state.set_state(mainState.state.state)


async def back_to_menu_call(callback: types.CallbackQuery, state):
    photo = types.InputFile('pictures/hello.jpg')
    await callback.message.answer_photo(photo=photo,
                                        caption=f'Добрый день {callback.message.chat.first_name} 😌 \nДобро пожаловать в "АВТО ТЕМА" \n\nНиже есть интерактивное меню, которое ответит на все ваши вопросы 👇🏼',
                                        reply_markup=keyboards.hello.keyboardMainMenu)
    await callback.answer()
    await state.finish()
    await state.set_state(mainState.state.state)


async def back_to_menu_msg(message: types.Message, state):
    photo = types.InputFile('pictures/hello.jpg')
    await message.answer_photo(photo=photo,
                               caption=f'Добрый день {message.chat.first_name} 😌 \nДобро пожаловать в "АВТО ТЕМА" \n\nНиже есть интерактивное меню, которое ответит на все ваши вопросы 👇🏼',
                               reply_markup=keyboards.hello.keyboardMainMenu)
    await state.finish()
    await state.set_state(mainState.state.state)


class mainState(StatesGroup):
    state = State()


# Калькулятор ----------------------------------------------------------------------------------------------------------
class calculator_call(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()


async def stage1_calculator(callback: types.CallbackQuery, state: calculator_call):
    photo = types.InputFile('pictures/calculator_hello.jpg')

    await callback.message.answer_photo(photo=photo,
                                        caption='Добро пожаловать в калькулятор.\n➖➖➖➖➖➖➖➖➖➖➖➖\n\nЯ помогу вам посчитать разницу между расходами с нашей клубной картой и без нее 👇🏼',
                                        reply_markup=keyboards.hello.keyboardMainCalculator)
    await callback.answer()
    await state.set_state(calculator_call.state1.state)


async def calculator_state1(callback: types.CallbackQuery, state: calculator_call):
    photo = types.InputFile('pictures/calculator1.jpg')
    await callback.message.answer_photo(photo=photo,
                                        caption=f'⛽️Напишите пожалуйста сколько вы тратите на бензин в месяц.\n\n*можете указать применую сумму')
    await callback.answer()
    await state.set_state(calculator_call.state2.state)


async def calculator_state2(message: types.Message, state: calculator_call):
    if is_float(message.text) == False:
        await message.answer('Нужно ввести число!')
        return
    await state.update_data(fuel=float(message.text))
    photo = types.InputFile('pictures/calculator2.jpg')
    await message.answer_photo(photo=photo,
                               caption=f'🛠 Сколько вы тратите на ТО в год?\n\n*можете указать примерную сумму',
                               )
    await state.set_state(calculator_call.state3.state)


async def calculator_state3(message: types.Message, state: calculator_call):
    if is_float(message.text) == False:
        await message.answer('Нужно ввести число!')
        return
    await state.update_data(to=float(message.text))
    photo = types.InputFile('pictures/calculator3.jpg')
    await message.answer_photo(photo=photo,
                               caption=f'🚘 Сколько у вас уходит в месяц на постоянные расходы? (мойка машины, покупка и замена резины и т.д.)\n\n*можете указать примерную сумму',
                               )
    await state.set_state(calculator_call.state4.state)


async def calculator_state4(message: types.Message, state: calculator_call):
    if is_float(message.text) == False:
        await message.answer('Нужно ввести число!')
        return
    await state.update_data(expenses=float(message.text))

    photo = types.InputFile('pictures/calculator4.jpg')
    await message.answer_photo(photo=photo,
                               caption=f'🆘 Сколько у вас может уйти в месяц на экстренные расходы? (эвакуатор, ремонт)\n\n*можете указать примерную сумму',
                               )
    await state.set_state(calculator_call.state5.state)


async def calculator_state5(message: types.Message, state: calculator_call):
    if is_float(message.text) == False:
        await message.answer('Нужно ввести число!')
        return
    await state.update_data(emergency=float(message.text))
    user_data = await state.get_data()
    discount = [0.9, 0.9, 0.85, 0.9]
    cur_sum = 0
    new_sum = 0
    j = 0
    for i in user_data:
        cur_sum += user_data[i]
        new_sum += user_data[i] * discount[j]
        j += 1
    await message.answer(
        text=f'Итого за год вы тратите на машину примерно: {math.ceil(cur_sum)} рублей\n\nУчаствуя в нашей программе, вы бы сэкономили {math.ceil(cur_sum - new_sum)} рублей , тратив на это 500 рублей в месяц\n\nИ потратили всего лишь {math.ceil(new_sum)} рублей \n\nЧтобы стать участником, нажимайте кнопку 👇🏼',
        reply_markup=keyboards.hello.keyboardEndCalculator)
    await state.set_state(calculator_call.state6.state)


# Как стать участником --------------------------------------------------------------------------------------------------
class how_to(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()


async def how_to_state1(callback: types.CallbackQuery, state):
    photo = types.InputFile('pictures/how_to1.jpg')
    await callback.message.answer_photo(photo=photo,
                                        caption=f'В нашем клубе Вы получите всю необходимую помощь от партнеров клуба.\n➖➖➖➖➖➖➖➖➖➖➖➖\nВся помощь от клуба делится на 2 программы: программа помощи на дорогах, программа скидок.⭐\nЧтобы стать участником клуба — необходимо приобрести карту клуба.',
                                        reply_markup=keyboards.hello.keyboardHowTo1)
    await callback.answer()
    await state.set_state(how_to.state1.state)


async def how_to_state2(callback: types.CallbackQuery, state):
    photo = types.InputFile('pictures/how_to2.jpg')
    await callback.message.answer_photo(photo=photo,
                                        caption=f'Стоимость участия в клубе: 500 рублей в месяц.\n*это в несколько раз ниже, чем скидка, которую вы получаете от партнеров.\n\nИмея карту участника клуба вы получаете доступ к скидке до 20% у партнёров.\n\nПосмотреть список партнеров по кнопке ниже или рассчитайте свою экономию от пользования с помощью нашего калькулятора  👇🏼',
                                        reply_markup=keyboards.hello.keyboardHowTo2)
    await callback.answer()
    await state.set_state(how_to.state2.state)


async def how_to_state3(callback: types.CallbackQuery, state):
    photo = types.InputFile('pictures/how_to3.jpg')
    await callback.message.answer_photo(photo=photo,
                                        caption=f'Что вы получите:\n- Скидки на автострахование\n- Скидки на услуги автосервиса\n- Скидки в магазинах водителей и помощь в подборе\n- Скидки на мойку автомобиля\n- Скидки на шиномонтаж\n- Скидки на услуги автоюриста\n- Помощь с оформлением ДТП\n\nЭто и многое другое со скидкой до 20% в нашем клубе 👇🏼',
                                        reply_markup=keyboards.hello.keyboardHowTo3)
    await callback.answer()
    await state.set_state(how_to.state3.state)


async def file_call(callback: types.CallbackQuery, state):
    file = types.InputFile('pictures/more.pdf')
    await callback.message.answer_document(document=file)
    await callback.answer()


# about
class about_state(StatesGroup):
    state1 = State()


async def about_call(callback: types.CallbackQuery, state):
    video = types.InputFile('pictures/video.mp4')
    await callback.message.answer_video(video=video,
                                        caption=f'Авто тема - это сообщество партнеров и участников (водителей)\n➖➖➖➖➖➖➖➖➖➖➖➖\nПартнеры - это проверенные организации, которые оказывают вам услуги со скидкой.\n➖➖➖➖➖➖➖➖➖➖➖➖\nНаша цель - это организовать большой клуб помощи водителям на дорогах и не только.',
                                        reply_markup=keyboards.hello.keyboardEndCalculator)
    await callback.answer()
    await state.set_state(about_state.state1.state)


# conctac
class contacts_state(StatesGroup):
    state1 = State()


async def contacts_call(callback: types.CallbackQuery, state):
    await callback.message.answer(text='📬По вопросу сотрудничества напишите пожалуйста @',
                                  reply_markup=keyboards.hello.keyboardBack)
    await callback.answer()
    await state.set_state(contacts_state.state1.state)


# todo УДАЛИТЬ УДАЛИТЬ УДАЛИТЬ УДАЛИТЬ УДЛАТЬ УДАЛИТЬ
from utils import vip_status


async def give_vip(message: types.Message):
    res = await vip_status.set_vip(message.chat.id, 30, message.chat.first_name)
    await message.answer('Успешно')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(reload, state='*', commands=['reload'])
    dp.register_message_handler(give_vip, state='*', commands=['vip'])

    # Менюшки
    dp.register_message_handler(hello_handler, state=None)
    dp.register_callback_query_handler(back_to_menu_call, state=None)

    # calculator
    dp.register_callback_query_handler(stage1_calculator, state=mainState.state, text_startswith='calculator')
    dp.register_callback_query_handler(back_to_menu_call, state=calculator_call.state1, text_startswith='back')

    dp.register_callback_query_handler(calculator_state1, state=calculator_call.state1, text_startswith='begin')
    dp.register_message_handler(calculator_state2, state=calculator_call.state2)
    dp.register_message_handler(calculator_state3, state=calculator_call.state3)
    dp.register_message_handler(calculator_state4, state=calculator_call.state4)
    dp.register_message_handler(calculator_state5, state=calculator_call.state5)
    dp.register_callback_query_handler(back_to_menu_call, state=calculator_call.state6, text_startswith='menu')
    dp.register_callback_query_handler(how_to_state1, state=calculator_call.state6, text_startswith='how_to')

    # how_to
    dp.register_callback_query_handler(how_to_state1, state=mainState.state, text_startswith='how_to')

    dp.register_callback_query_handler(how_to_state2, state=how_to.state1, text_startswith='more')
    dp.register_callback_query_handler(back_to_menu_call, state=how_to.state1, text_startswith='menu')
    # todo редирект на pay
    # dp.register_callback_query_handler(how_to_state2, state=how_to.state1, text='pay')

    dp.register_callback_query_handler(how_to_state3, state=how_to.state2, text_startswith='more')
    dp.register_callback_query_handler(stage1_calculator, state=how_to.state2, text_startswith='calculator')
    dp.register_callback_query_handler(how_to_state1, state=how_to.state2, text_startswith='back')

    # todo редирект на pay
    # dp.register_callback_query_handler()
    dp.register_callback_query_handler(file_call, state=how_to.state3, text_startswith='file')
    dp.register_callback_query_handler(how_to_state2, state=how_to.state3, text_startswith='back')

    # about
    dp.register_callback_query_handler(about_call, state=mainState.state, text_startswith='about')

    dp.register_callback_query_handler(how_to_state1, state=about_state.state1, text_startswith='how_to')
    dp.register_callback_query_handler(back_to_menu_call, state=about_state.state1, text_startswith='menu')

    # contacts
    dp.register_callback_query_handler(contacts_call, state=mainState.state, text_startswith='collaboration')

    dp.register_callback_query_handler(back_to_menu_call, state=contacts_state.state1, text_startswith='menu')


