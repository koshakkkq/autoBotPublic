from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import admin
from utils import category
#если не оплатил
inline_btn_1 = InlineKeyboardButton('⚡️Вступить в клуб⚡️', callback_data='pay')
inline_btn_2 = InlineKeyboardButton('Назад ↩', callback_data='menu')
keyboardNotVip= InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)

#главное меню
inline_btn_1 = InlineKeyboardButton('ВАШ ЛИЧНЫЙ КАБИНЕТ 👨🏼‍💻', callback_data='account')
keyboardMenu = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_btn_2 = InlineKeyboardButton('Продлить подписку ✅', callback_data='pay')
inline_btn_3 = InlineKeyboardButton('📍Список партнёров', callback_data='partners')
keyboardMenu.add(inline_btn_2, inline_btn_3)
inline_btn_4 = InlineKeyboardButton('НАШ КАНАЛ 💭', url='yandex.ru')
inline_btn_5 = InlineKeyboardButton('⚡️ОНЛАЙН ПОМОЩЬ⚡️', callback_data='search_partners')
keyboardMenu.add(inline_btn_4, inline_btn_5)

keyboardMenu = {False:keyboardMenu, True:admin.keyboardMenu}


#аккаунт
inline_btn_1 = InlineKeyboardButton('🟡Подробнее про реферальнкую систему🟡', callback_data='ref')
inline_btn_2 = InlineKeyboardButton('Назад ↩', callback_data='back')
keyboardAccount= InlineKeyboardMarkup(row_width=1).add(inline_btn_1, inline_btn_2)
#стра

keyboardEmpty = InlineKeyboardMarkup()

async def get_cities_keyboard(cur_page, is_admin):
    cities = await category.get_cities((cur_page-1)*3)
    cities_cnt = await category.get_cities_count()
    keyboard = InlineKeyboardMarkup(row_width=3)
    if cities[0] == False or cities_cnt[0] == False:
        return False
    for i in cities[1]:

        inline_btn_1 = InlineKeyboardButton(i, callback_data='city_pick_'+str(i))
        keyboard.add(inline_btn_1)
    inline_btn_2 = InlineKeyboardButton('➡', callback_data='next_cities')

    max_page = (cities_cnt[1]+2)//3

    inline_btn_1 = InlineKeyboardButton(f'{cur_page}/{max_page}', callback_data='kekekek')

    inline_btn_3 = InlineKeyboardButton('⬅', callback_data='prev_cities')
    if max_page <= 1:
        pass
    elif cur_page == max_page:
        keyboard.add(inline_btn_3, inline_btn_1, )
    elif cur_page == 1:
        keyboard.add(inline_btn_2, inline_btn_1)
    else:
        keyboard.add(inline_btn_3, inline_btn_1,inline_btn_2)

    if is_admin:
        inline_btn_3 = InlineKeyboardButton('Добавить➕', callback_data='add_city')
        keyboard.add(inline_btn_3)

    inline_btn_3 = InlineKeyboardButton('В меню↩', callback_data='menu')
    keyboard.add(inline_btn_3)
    return keyboard

async def get_category_keyboard(cur_page, city, is_admin):
    categories = await category.get_categories(skipped = (cur_page-1)*6, city = city)
    categoriesCnt = await category.get_categories_count(city)

    categoriesBtn = []

    if categories[0] == False or categoriesCnt[0] == False:
        return False
    for i in range(0, len(categories[1]), 2):
        if i+1 == len(categories[1]):
            categoriesBtn.append([InlineKeyboardButton(categories[1][i], callback_data='category_pick'+'_'+str(categories[1][i]))])
        else:
            categoriesBtn.append([InlineKeyboardButton(categories[1][i], callback_data='category_pick'+'_'+str(categories[1][i])), InlineKeyboardButton(categories[1][i+1], callback_data='category_pick_'+str(categories[1][i+1]))])


    maxPage = (categoriesCnt[1]+5)//6

    inline_btn_1 = InlineKeyboardButton(f'{cur_page}/{maxPage}', callback_data='kekekek')

    inline_btn_2 = InlineKeyboardButton('➡', callback_data='next')
    inline_btn_3 = InlineKeyboardButton('⬅', callback_data='prev')
    if maxPage <= 1:
        pass
    elif cur_page == maxPage:
        categoriesBtn.append([inline_btn_3, inline_btn_1])
    elif cur_page == 1:
        categoriesBtn.append([inline_btn_2, inline_btn_1])
    else:
        categoriesBtn.append([inline_btn_3, inline_btn_1, inline_btn_2])

    if is_admin:
        inline_btn_3 = InlineKeyboardButton('Добавить➕', callback_data='add')
        inline_btn_4 = InlineKeyboardButton('Удалить❌', callback_data='delete')
        categoriesBtn.append([inline_btn_3, inline_btn_4])

    inline_btn_3 = InlineKeyboardButton('Назад↩', callback_data='back')
    categoriesBtn.append([inline_btn_3])
    resKeyboard = InlineKeyboardMarkup(inline_keyboard=categoriesBtn)


    return resKeyboard


async def get_partner_keyboard(cur_page, city,categoryName, is_admin):
    categories = await category.get_partners(skipped = (cur_page-1)*6, city = city, category=categoryName)
    categoriesCnt = await category.get_partners_count(city = city, category = categoryName)

    categoriesBtn = []

    if categories[0] == False or categoriesCnt[0] == False:
        return False
    for i in range(0, len(categories[1]), 2):
        if i+1 == len(categories[1]):
            categoriesBtn.append([InlineKeyboardButton(categories[1][i], callback_data='partner_pick'+'_'+str(categories[1][i]))])
        else:
            categoriesBtn.append([InlineKeyboardButton(categories[1][i], callback_data='partner_pick'+'_'+str(categories[1][i])), InlineKeyboardButton(categories[1][i+1], callback_data='partner_pick_'+str(categories[1][i+1]))])


    maxPage = (categoriesCnt[1]+5)//6

    inline_btn_1 = InlineKeyboardButton(f'{cur_page}/{maxPage}', callback_data='kekekek')

    inline_btn_2 = InlineKeyboardButton('➡', callback_data='next')
    inline_btn_3 = InlineKeyboardButton('⬅', callback_data='prev')
    if maxPage <= 1:
        pass
    elif cur_page == maxPage:
        categoriesBtn.append([inline_btn_3, inline_btn_1])
    elif cur_page == 1:
        categoriesBtn.append([inline_btn_2, inline_btn_1])
    else:
        categoriesBtn.append([inline_btn_3, inline_btn_1, inline_btn_2])

    if is_admin:
        inline_btn_3 = InlineKeyboardButton('Добавить➕', callback_data='add')
        inline_btn_4 = InlineKeyboardButton('Удалить❌', callback_data='delete')
        categoriesBtn.append([inline_btn_3, inline_btn_4])

    inline_btn_3 = InlineKeyboardButton('Назад↩', callback_data='back')
    categoriesBtn.append([inline_btn_3])
    resKeyboard = InlineKeyboardMarkup(inline_keyboard=categoriesBtn)


    return resKeyboard

