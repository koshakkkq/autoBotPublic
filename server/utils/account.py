import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime

users = db.users


async def get_user_info(id):
    res = await users.find_one({'id': id})
    if res == None:
        return None
    dateS = datetime.utcfromtimestamp(res['vipTill']).strftime('%Y-%m-%d')
    s = f'Добро пожаловать в ваш личный кабинет\n\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n📅\n\nВаша подписка до: {dateS}\n\n🔗 Ваша реферальная ссылка: *ссылка*\n\n👥 Вы пригласили: 0 друзей'
    return s
