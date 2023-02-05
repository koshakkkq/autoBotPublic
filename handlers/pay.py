from aiogram.dispatcher.filters.state import State, StatesGroup
from create import dp, bot
from aiogram import types, Dispatcher
from aiogram.types.message import ContentType
from create import payToken
from utils import vip_status
import keyboards

class payState(StatesGroup):
    info = State()
    invoice = State()


async def pay_info(callback: types.CallbackQuery, state):
    PRICE = types.LabeledPrice(label='Vip подписка на 1 месяц', amount=50000)
    await bot.send_invoice(
        callback.message.chat.id,
        title='Оформить vip',
        description='Стоимость ежемесячного платежа: 500 рублей (это 17 рублей в день).\n\nВыберите удобный способ оплаты 👇🏼(это тестовый вариант без оплаты,используйте ревезиты : 1111 1111 1111 1026, 12/22, CVC 000',
        provider_token=payToken,
        currency='rub',
        is_flexible=False,
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use', reply_markup=keyboards.hello.keyboardPay)

    await callback.answer()

async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: types.Message):
    res = await vip_status.set_vip(message.chat.id, 30, message.chat.first_name)
    if res == False:
        await message.answer('Произошла ошибка, пожалуйста обратитесь к Админу @')
    else:
        await message.answer(
        text='Поздравляю!🥳🥳🥳\n\n🔗 Ссылка на канал: *ссылка*\n\nВведите команду /auto, чтобы открыть дополнительное меню со всеми возможностями в боте.')


def register_handlers_client(dp: Dispatcher):
    # Редирект в pay
    dp.register_callback_query_handler(pay_info, state='*', text_startswith='pay')

    # оплатка
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, lambda query: True, state='*')
    dp.register_message_handler(process_successful_payment, state='*', content_types=ContentType.SUCCESSFUL_PAYMENT)