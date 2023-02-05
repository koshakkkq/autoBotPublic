import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime
from mailing.messages_operations import  add_msg
users = db.users
wasInBot = db.was_in_bot


async def get_user_info(id):
    res = await users.find_one({'id': id})
    if res == None:
        return None
    dateS = datetime.utcfromtimestamp(res['vipTill']).strftime('%Y-%m-%d')
    s = f'<b>Добро пожаловать в ваш личный кабинет\n\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n📅\n\nВаша подписка до: {dateS}\n\n🔗 Ваша реферальная ссылка: *ссылка*\n\n👥 Вы пригласили: 0 друзей</b>'
    return s


async def was_in_bot(id):
    cnt = await wasInBot.count_documents({'id':id})
    await users.update_one({'id':id}, {'$setOnInsert':{'vipTill':0}}, upsert=True)
    if cnt == 0:
        await add_msg(id, 'helloMsg1')
        await wasInBot.insert_one({'id':id})
    return True