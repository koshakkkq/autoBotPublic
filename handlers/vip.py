from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

import utils.category
from create import dp
from handlers.hello import mainState, back_to_menu_call
from utils import vip_status
from create import adminId
from utils import admin
import keyboards

#todo нормальная возврат на туже страницу
class isVipState(StatesGroup):
    inVipMenu = State()
    inAdsMenu = State()

class vipMenu(StatesGroup):
    account = State()
    moreAboutRef = State()
    partners = State()
    partners_search = State()


#Менюшки ---------------------------------------------------------------------------------------------------------------
async def vip_menu(callback: types.CallbackQuery, state):
    await state.finish()
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    else:
        await callback.message.answer(text='Добро пожаловать в клубный бот! 🤖\n\nВсе необходимое вы сможете найти в меню ниже 👇🏼',
                                      reply_markup=keyboards.vip.keyboardMenu[callback.message.chat.id == adminId])
        await state.set_state(isVipState.inVipMenu.state)
        await callback.answer()
        return

async def vip_menu_msg(message: types.Message, state):
    await state.finish()
    is_vip = await vip_status.is_vip(message.chat.id)
    if is_vip == False:
        await isNotVipMsg(message, state)
        return
    else:
        await message.answer(text='Добро пожаловать в клубный бот! 🤖\n\nВсе необходимое вы сможете найти в меню ниже 👇🏼',
                                      reply_markup=keyboards.vip.keyboardMenu[message.chat.id == adminId])
        await state.set_state(isVipState.inVipMenu.state)
        return

async def isNotVip(callback: types.CallbackQuery, state):
    await state.finish()
    await callback.message.answer(
        text='🗝 Закрытый клуб для автолюбителей\n\nУ нас вы найдете:\n\n- скидки и проверенных партнеров - окружение, кто вас понимает\n- поддержку 24/7\n- свежие новости\n\n💰 Стоимость участия: 500 рублей в мес.',
        reply_markup=keyboards.vip.keyboardNotVip)
    await state.set_state(isVipState.inAdsMenu.state)
    await callback.answer()
    return

async def isNotVipMsg(message, state):
    await state.finish()
    await message.answer(
        text='🗝 Закрытый клуб для автолюбителей\n\nУ нас вы найдете:\n\n- скидки и проверенных партнеров - окружение, кто вас понимает\n- поддержку 24/7\n- свежие новости\n\n💰 Стоимость участия: 500 рублей в мес.',
        reply_markup=keyboards.vip.keyboardNotVip)
    await state.set_state(isVipState.inAdsMenu.state)
    return

#cities --------------------------------------------------------------------------------------------------------------

class partnersStates(StatesGroup):
    city = State()
    category = State()
    partners = State()
    partnersInfo = State()


async def cities_call(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    keyboard = await keyboards.vip.get_cities_keyboard(1, callback.message.chat.id == adminId)
    await state.update_data(cityPage=1)
    await callback.message.answer(
        text='Выберите пожалуйста ваш город 🌆',
        reply_markup=keyboard)
    await state.set_state(partnersStates.city.state)
    await callback.answer()

async def cities_next(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    user_data = await state.get_data()
    await state.update_data(cityPage= user_data['cityPage'] + 1)
    keyboard = await keyboards.vip.get_cities_keyboard(user_data['cityPage'] + 1, callback.message.chat.id == adminId)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

async def cities_prev(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    user_data = await state.get_data()
    await state.update_data(cityPage= user_data['cityPage'] - 1)
    keyboard = await keyboards.vip.get_cities_keyboard(user_data['cityPage'] - 1, callback.message.chat.id == adminId)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


#admin-city------------------------------------------------------------------------------------------------------------------

class citiesAdd(StatesGroup):
    adding = State()
    stop = State()

async def cities_call_admin(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    await callback.message.answer(
        text='Введите название города который хотите добавить!',
        reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(citiesAdd.adding.state)

async def cities_get_name(message: types.Message, state):
    if message.chat.id != adminId:
        return
    name = message.text
    res = await admin.add_citie(name)
    status = 'Ошибка, нажмите назад.'
    if res == True:
        status = 'Успешно!, нажмите назад.'

    await message.answer(text=status, reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(citiesAdd.stop.state)


async def delete_city(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return

    userData = await state.get_data()
    res = await admin.delete_city(userData['cityId'])
    resTxt = 'Ошбика'
    if res == True:
        resTxt = 'Успешно'

    keyboard = await keyboards.vip.get_cities_keyboard(1, callback.message.chat.id == adminId)
    await state.update_data(cityPage=1)
    await callback.message.answer(
        text='Выберите пожалуйста ваш город 🌆',
        reply_markup=keyboard)
    await state.set_state(partnersStates.city.state)

    await callback.answer(resTxt)



#category

async def city_pick(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    cityId = callback.data.split('_')[-1]
    await state.update_data(cityId = cityId)
    city = await utils.category.get_city_name_by_id(cityId)
    if city == None:
        return
    await state.update_data(city = city)
    await callback.message.edit_text(f'Выбран город: {city} 🌆')
    #await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)

    keyboard = await keyboards.vip.get_category_keyboard(1, cityId, callback.message.chat.id == adminId)

    await callback.message.answer(f'🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.', reply_markup=keyboard)


    await callback.answer(f'Выбран город: {city} 🌆')
    await state.set_state(partnersStates.category.state)
    await state.update_data(categoryPage=1)


async def city_show_info(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    userData = await state.get_data()
    city = userData['city']
    await callback.message.edit_text(f'Выбран город: {city} 🌆')
    # await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)

    keyboard = await keyboards.vip.get_category_keyboard(1, userData['cityId'], callback.message.chat.id == adminId)

    await callback.message.answer(f'🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.',
                                  reply_markup=keyboard)

    await callback.answer(f'Выбран город: {city} 🌆')
    await state.set_state(partnersStates.category.state)
    await state.update_data(categoryPage=1)


async def categories_next(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    user_data = await state.get_data()
    await state.update_data(categoryPage= user_data['categoryPage'] + 1)
    keyboard = await keyboards.vip.get_category_keyboard(cur_page=user_data['categoryPage'] + 1, city=user_data['cityId'],
                                                         is_admin=callback.message.chat.id == adminId)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


async def categories_prev(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    user_data = await state.get_data()
    await state.update_data(categoryPage=user_data['categoryPage'] - 1)
    keyboard = await keyboards.vip.get_category_keyboard(cur_page=user_data['categoryPage'] - 1, city=user_data['cityId'],
                                                         is_admin=callback.message.chat.id == adminId)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


async def category_call(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    userData = await state.get_data()
    city = userData['city']

    # await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)

    keyboard = await keyboards.vip.get_category_keyboard(1, userData['cityId'], callback.message.chat.id == adminId)

    await callback.message.answer(f'Выбран город: {city} 🌆')
    await callback.message.answer(f'🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.',
                                  reply_markup=keyboard)

    await state.set_state(partnersStates.category.state)
    await state.update_data(categoryPage=1)


#category_admin---------------------------------------------------------------------------------------------------------
class categoryAdd(StatesGroup):
    adding = State()
    stop = State()
    addTag = State()


async def category_add(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    await callback.message.answer(
        text='Введите название категории которую хотите добавить!',
        reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(categoryAdd.adding.state)
    await callback.answer()

#
async def tag_add(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    await callback.message.answer(text='Введите ключевое слово или запрос для этой категории',
        reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(categoryAdd.addTag.state)
    await callback.answer()

async def tag_get_name(message: types.Message, state):
    if message.chat.id != adminId:
        return
    name = message.text
    userData = await state.get_data()
    res = await admin.add_category_tag(userData['cityId'], userData['categoryId'], name, userData['category'])
    status = 'Ошибка, нажмите назад.'
    if res == True:
        status = 'Успешно!, нажмите назад.'

    await message.answer(text=status, reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(partnerAdd.stop.state)

async def category_get_name(message: types.Message, state):
    if message.chat.id != adminId:
        return
    name = message.text
    userData = await state.get_data()
    res = await admin.add_category(name=name, city=userData['cityId'])
    status = 'Ошибка, нажмите назад.'
    if res == True:
        status = 'Успешно!, нажмите назад.'

    await message.answer(text=status, reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(categoryAdd.stop.state)

async def delete_category(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return

    userData = await state.get_data()
    res = await admin.delete_category(cityId=userData['cityId'], categoryId=userData['categoryId'])
    resTxt = 'Ошбика'
    if res == True:
        resTxt = 'Успешно'

    keyboard = await keyboards.vip.get_category_keyboard(cur_page=1,city=userData['cityId'], is_admin = callback.message.chat.id == adminId)
    await state.update_data(categoryPage=1)
    await callback.message.answer(
        text='🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.',
        reply_markup=keyboard)
    await state.set_state(partnersStates.category.state)

    await callback.answer(resTxt)


#partner-----------------------------
async def pick_category(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    userData = await state.get_data()
    categoryId = callback.data.split('_')[-1]
    await state.update_data(categoryId=categoryId)
    categoryName = await category.get_category_by_id(categoryId)
    await callback.message.edit_text(f'Выбрана категория: {categoryName} ')
    await state.update_data(category=categoryName)
    # await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)

    myKeyboard = await keyboards.vip.get_partner_keyboard(1, city=userData['cityId'],categoryId=categoryId , is_admin=callback.message.chat.id == adminId)

    await callback.message.answer(f'🔎 Наши партнеры в этой категории.',
                                  reply_markup=myKeyboard)

    await callback.answer(f'Выбрана категория: {categoryName} ')
    await state.set_state(partnersStates.partners.state)
    await state.update_data(partnersPage=1)



async def partners_next(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    user_data = await state.get_data()
    await state.update_data(partnersPage = user_data['partnersPage'] + 1)
    keyboard = await keyboards.vip.get_partner_keyboard(cur_page=user_data['partnersPage'] + 1, city=user_data['cityId'],
                                                        categoryId=user_data['categoryId'],
                                                        is_admin=callback.message.chat.id == adminId)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


async def partners_prev(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    user_data = await state.get_data()
    await state.update_data(partnersPage = user_data['partnersPage'] - 1)
    keyboard = await keyboards.vip.get_partner_keyboard(cur_page=user_data['partnersPage'] - 1, city=user_data['cityId'],
                                                        categoryId=user_data['categoryId'],
                                                        is_admin=callback.message.chat.id == adminId)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


async def show_partners(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    userData = await state.get_data()
    category = userData['category']
    await callback.message.answer(f'Выбрана категория: {category} ')
    # await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)

    myKeyboard = await keyboards.vip.get_partner_keyboard(userData['partnersPage'], city=userData['cityId'],categoryId=userData['categoryId'] , is_admin=callback.message.chat.id == adminId)

    await callback.message.answer(f'🔎 Наши партнеры в этой категории.',
                                  reply_markup=myKeyboard)

    await callback.answer(f'Выбрана категория: {category} ')
    await state.set_state(partnersStates.partners.state)

#partner admin----------------------------


class partnerAdd(StatesGroup):
    addingName = State()
    addingInfo = State()
    stop = State()


async def partner_add(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    await callback.message.answer(
        text='Введите имя партнёра(оно будет отражаться на кнопке)',
        reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(partnerAdd.addingName.state)
    await callback.answer()


async def partner_get_name(message: types.message,state):
    if message.chat.id != adminId:
        return
    name = message.text
    await state.update_data(partnerName=name)
    await state.set_state(partnerAdd.addingInfo.state)
    await message.answer(
        text='Введите подробную информацию о партнёре и добавьте фото',
        reply_markup=keyboards.admin.keyboardBack)

async def partner_get_info(message: types.Message, state):
    if message.chat.id != adminId:
        return
    text = message.text
    photo = None
    userData = await state.get_data()
    res = await admin.add_partner(category=userData['categoryId'], city=userData['cityId'], photo=photo, text = text,
                                  name = userData['partnerName'])
    status = 'Ошибка, нажмите назад.'
    if res == True:
        status = 'Успешно!, нажмите назад.'

    await message.answer(text=status, reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(partnerAdd.stop.state)

async def partner_get_info_with_photo(message: types.Message, state):
    if message.chat.id != adminId:
        return
    text = message.caption
    photo = message.photo[-1].file_id
    userData = await state.get_data()
    res = await admin.add_partner(category=userData['categoryId'], city=userData['cityId'], photo=photo, text = text,
                                  name = userData['partnerName'])
    status = 'Ошибка, нажмите назад.'
    if res == True:
        status = 'Успешно!, нажмите назад.'

    await message.answer(text=status, reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(partnerAdd.stop.state)


#partners-pick
#todo возврат
from utils import category
async def pick_partner(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    userData = await state.get_data()
    partnerId = callback.data.split('_')[-1]
    await state.update_data(partnerId=partnerId)
    res = await category.get_partner_info(cityName=userData['cityId'], partnerId=partnerId, categoryName=userData['categoryId'])
    await state.update_data(partnerName = res['name'])
    if res['photo'] is not None:
        await callback.message.answer_photo(photo=res['photo'], caption=res['text'], reply_markup=keyboards.admin.keyBack[callback.message.chat.id == adminId])
    else:
        await callback.message.answer(text=res['text'], reply_markup=keyboards.admin.keyBack[callback.message.chat.id == adminId])
    await state.set_state(partnersStates.partnersInfo.state)
    await callback.answer()




class searching(StatesGroup):
    state1 = State()
    searching = State()

async def partner_search_city_pick(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    keyboard = await keyboards.vip.get_cities_keyboard(1, False)
    await state.update_data(cityPage=1)
    await callback.message.answer(
        text='Выберите пожалуйста ваш город 🌆',
        reply_markup=keyboard)
    await state.set_state(vipMenu.partners_search.state)
    await callback.answer()

async def partner_search_menu(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    cityId = callback.data.split('_')[-1]
    await state.update_data(cityId=cityId)
    city = await utils.category.get_city_name_by_id(cityId)
    if city == None:
        return
    await state.update_data(city=city)
    await callback.message.edit_text(f'Выбран город: {city} 🌆')
    # await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)


    await callback.message.answer(f'🔎 Напишите, что вам необходимо найти.',
                                  reply_markup=keyboards.vip.keyboardPartnerSearch)

    await callback.answer(f'Выбран город: {city} 🌆')
    await state.set_state(searching.searching.state)
    await state.update_data(categoryPage=1)


async def partner_search(message: types.Message, state):
    is_vip = await vip_status.is_vip(message.chat.id)
    if is_vip == False:
        await isNotVip(message, state)
        return
    req = message.text
    userData = await state.get_data()
    resKeyboard = await keyboards.vip.get_category_by_search(city=userData['cityId'], req=req, cur_page=1, is_admin=False)
    await state.update_data(req = req)
    if resKeyboard is None:
        keyboard = await keyboards.vip.get_category_keyboard(1, userData['cityId'], message.chat.id == adminId)
        await message.answer(f'К сожалению ничего не найдено, попробуйте найти вручную\n\nВыбран город: {userData["city"]} 🌆')
        await message.answer(f'🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.',
                                      reply_markup=keyboard)

        await state.set_state(partnersStates.category.state)
        await state.update_data(categoryPage=1)
    else:

        await message.answer(f'🔎 Выберите необходимую категорию.',
                             reply_markup=resKeyboard)
        await state.update_data(categorySearchPage = 1)
        await state.set_state(searching.state1)

async def next_search_page(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    userData = await state.get_data()
    resKeyboard = await keyboards.vip.get_category_by_search(city=userData['cityId'], req=userData['req'], cur_page=userData['categorySearchPage'] +1 )
    if resKeyboard is None:
        keyboard = await keyboards.vip.get_category_keyboard(1, userData['cityId'], callback.message.chat.id == adminId)
        await callback.message.answer(f'К сожадению ничего не найдено, попробуйте найти вручную\n\nВыбран город: {userData["city"]} 🌆')
        await callback.message.answer(f'🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.',
                                      reply_markup=keyboard)

        await state.set_state(partnersStates.category.state)
    else:

        await callback.message.answer(f'🔎 Выберите необходимую категорию.',
                             reply_markup=resKeyboard)
        await state.update_data(userData['categorySearchPage']+1)
        await state.set_state(searching.state1)
    await callback.answer()

async def prev_search_page(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    userData = await state.get_data()
    resKeyboard = await keyboards.vip.get_category_by_search(city=userData['cityId'], req=userData['req'], cur_page=userData['categorySearchPage'] -1 )
    if resKeyboard is None:
        keyboard = await keyboards.vip.get_category_keyboard(1, userData['cityId'], callback.message.chat.id == adminId)
        await callback.message.answer(f'К сожалению ничего не найдено, попробуйте найти вручную!\n\nВыбран город: {userData["city"]} 🌆')
        await callback.message.answer(f'🔎 Выберите необходимую категорию или напишите, что вам необходимо найти.',
                                      reply_markup=keyboard)

        await state.set_state(partnersStates.category.state)
    else:

        await callback.message.answer(f'🔎 Выберите необходимую категорию.',
                             reply_markup=resKeyboard)
        await state.update_data(userData['categorySearchPage']-1)
        await state.set_state(searching.state1)
    await callback.answer()

async def delete_partner(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    userData = await state.get_data()
    res = await admin.delete_partner(city=userData['cityId'], name=userData['partnerId'], category=userData['categoryId'])
    status = 'Ошибка'
    if res == True:
        status = 'Успешно'

    await callback.message.answer(f"{status}\nВыбрана категория: {userData['category']}")
    # await callback.message.edit_reply_markup(reply_markup=keyboards.vip.keyboardEmpty)

    myKeyboard = await keyboards.vip.get_partner_keyboard(userData['partnersPage'], city=userData['cityId'],
                                                        categoryId=userData['categoryId'],
                                                        is_admin=callback.message.chat.id == adminId)

    await callback.message.answer(f'🔎 Наши партнеры в этой категории.',
                                  reply_markup=myKeyboard)

    await callback.answer(f'Выбрана категория: {userData["category"]} ')
    await state.set_state(partnersStates.partners.state)

#acounts----------------------------------------------------------------------------------------------------------------
from utils import account

async def get_account(callback: types.CallbackQuery, state):
    is_vip = await vip_status.is_vip(callback.message.chat.id)
    if is_vip == False:
        await isNotVip(callback, state)
        return
    ans = await account.get_user_info(callback.message.chat.id)
    if ans == None:
        return
    await callback.message.answer(text=ans, reply_markup=keyboards.vip.keyboardAccount, parse_mode=types.ParseMode.HTML)
    await state.set_state(vipMenu.account.state)

async def more_about_ref(callback: types.CallbackQuery, state):
    await callback.message.answer(text='🔗Условия реферальной системы\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n1. Пригласи друзей в бота и получи 10% от ее оплат на свой счет.\n\n2. При оплате, ты сможешь оплатить подписку бонусами, а не рублями', reply_markup=keyboards.admin.keyboardBack)
    await state.set_state(vipMenu.moreAboutRef.state)



#search
class MailingAdmin(StatesGroup):
 addText = State()
async def mailing_admin(callback: types.CallbackQuery, state):
    if callback.message.chat.id != adminId:
        return
    to = callback.data.split('_')[2]
    if to == 'vip':
        await state.update_data(mailingToVip=True)
    else:
        await state.update_data(mailingToVip=False)

    await callback.message.answer('Введите текст расслыки', reply_markup=keyboards.admin.keyboardBack)
    await callback.answer()
    await state.set_state(MailingAdmin.addText.state)

async def mailing_text(message: types.Message, state):
    if message.chat.id != adminId:
        return
    text = message.text
    user_data = await state.get_data()
    await message.answer('Рассылка началась', reply_markup=keyboards.admin.keyboardBack)
    await admin.mailing_admin(text, user_data['mailingToVip'])


def register_handlers_client(dp: Dispatcher):
    #Редирект в меню vip
    dp.register_callback_query_handler(vip_menu, state=mainState.state, text_startswith='vip')
    dp.register_callback_query_handler(back_to_menu_call, state=isVipState.inAdsMenu, text_startswith = 'menu')
    dp.register_message_handler(vip_menu_msg, state='*', commands=['auto'])

    #todo редирект на pay
    #dp.register_callback_query_handler(back_to_menu_call, state=isVipState.inAdsMenu, text_startswith = 'pay')

    #partners
    #city
    dp.register_callback_query_handler(cities_call, state=isVipState.inVipMenu, text_startswith = 'partners')
    dp.register_callback_query_handler(cities_next, state=partnersStates.city, text_startswith='next_cities')
    dp.register_callback_query_handler(cities_prev, state=partnersStates.city, text_startswith='prev_cities')
    dp.register_callback_query_handler(vip_menu, state=partnersStates.city, text_startswith='menu')
    dp.register_callback_query_handler(city_pick, state=partnersStates.city, text_startswith='city_pick_')

    #admin-city
    dp.register_callback_query_handler(cities_call, state=citiesAdd.adding, text_startswith='back')
    dp.register_callback_query_handler(cities_call_admin, state=partnersStates.city, text_startswith='add_city')
    dp.register_message_handler(cities_get_name, state=citiesAdd.adding)
    dp.register_callback_query_handler(cities_call, state=citiesAdd.stop)

    #category
    dp.register_callback_query_handler(city_pick, state=partnersStates.city, text_startswith='back')
    dp.register_callback_query_handler(categories_next, state=partnersStates.category, text_startswith='next')
    dp.register_callback_query_handler(categories_prev, state=partnersStates.category, text_startswith='prev')
    dp.register_callback_query_handler(cities_call, state=partnersStates.category, text_startswith='back')
    dp.register_message_handler(partner_search, state=partnersStates.category)

    #admin-category
    dp.register_callback_query_handler(category_add, state=partnersStates.category, text_startswith='add')
    dp.register_message_handler(category_get_name, state= categoryAdd.adding)
    dp.register_callback_query_handler(city_show_info, state= categoryAdd.stop)
    dp.register_callback_query_handler(delete_city, state= partnersStates.category, text_startswith='delete')
    dp.register_callback_query_handler(category_call, state=categoryAdd.adding, text_startswith='back')

    dp.register_callback_query_handler(tag_add, state=partnersStates.partners, text_startswith='tag_add')
    dp.register_message_handler(tag_get_name, state=categoryAdd.addTag)


    #partner
    dp.register_callback_query_handler(pick_category, state=partnersStates.category, text_startswith='category_pick')
    dp.register_callback_query_handler(partners_prev, state=partnersStates.partners, text_startswith='prev')
    dp.register_callback_query_handler(partners_next, state=partnersStates.partners, text_startswith='next')
    dp.register_callback_query_handler(category_call, state=partnersStates.partners, text_startswith='back')


    #admin-partner
    dp.register_callback_query_handler(partner_add, state=partnersStates.partners, text_startswith='add')

    dp.register_message_handler(partner_get_name, state=partnerAdd.addingName)
    dp.register_message_handler(partner_get_info, state=partnerAdd.addingInfo)
    dp.register_message_handler(partner_get_info_with_photo, state=partnerAdd.addingInfo, content_types=['photo'])
    dp.register_callback_query_handler(show_partners, state=partnerAdd.stop)
    dp.register_callback_query_handler(delete_category, state=partnersStates.partners, text_startswith='delete')
    dp.register_callback_query_handler(show_partners, state=partnerAdd.addingName, text_startswith='back')

    #partner-info
    dp.register_callback_query_handler(pick_partner, state=partnersStates.partners, text_startswith='partner_pick')
    dp.register_callback_query_handler(show_partners, state=partnersStates.partnersInfo, text_startswith='back')

    #partner-delete
    dp.register_callback_query_handler(delete_partner, state=partnersStates.partnersInfo, text_startswith='delete')


    #-------------------------------------------------------------------------------------------------------------------
    #accoutn
    #main_page_acount
    dp.register_callback_query_handler(get_account, state=isVipState.inVipMenu, text_startswith='account')
    dp.register_callback_query_handler(vip_menu, state=vipMenu.account, text_startswith='back')
    dp.register_callback_query_handler(get_account, state=vipMenu.moreAboutRef, text_startswith='back')
    dp.register_callback_query_handler(more_about_ref, state=vipMenu.account,  text_startswith='ref')

    #partner_serach
    dp.register_callback_query_handler(partner_search_city_pick, state=isVipState.inVipMenu, text_startswith='search_partners')
    dp.register_callback_query_handler(partner_search_menu, state=vipMenu.partners_search, text_startswith='city_pick_')
    dp.register_message_handler(partner_search, state=searching.searching)
    dp.register_callback_query_handler(next_search_page, state = searching.state1, text_startswith='next')
    dp.register_callback_query_handler(prev_search_page, state = searching.state1, text_startswith='prev')

    dp.register_callback_query_handler(vip_menu, state=vipMenu.partners_search.state, text_startswith='menu')
    dp.register_callback_query_handler(partner_search_city_pick, state = searching.searching, text_startswith = 'back')
    dp.register_callback_query_handler(vip_menu, state=searching.state1,text_startswith='back' )
    dp.register_callback_query_handler(pick_category, state=searching.state1, text_startswith='category_pick')

    dp.register_callback_query_handler(mailing_admin, state=isVipState.inVipMenu, text_startswith='send_to')
    dp.register_message_handler(mailing_text, state=MailingAdmin.addText)
    dp.register_callback_query_handler(vip_menu,  state=MailingAdmin.addText)