import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime

users = db.users


async def set_vip(id, days):
    try:
        document = await users.find_one({'id': id})
    except Exception as e:
        logging.error(e)
        return False
    cur_time = 0
    if document is not None:
        cur_time = document['vipTill']
    try:
        cur_time = max(int(time.time()), cur_time)
        vipTill = cur_time + days * 24 * 60 * 60
        add = {'id': id, 'vipTill': vipTill}
        await users.update_one({'id': id}, {'$set': add }, upsert=True)
        return False
    except Exception as e:
        logging.error(e)
        return False


async def is_vip(id):
    try:
        document = await users.find_one({'id':id})
        if document is None:
            return False
        return await is_vip_time(document['vipTill'])
    except Exception as e:
        logging.error(e)
        return False

async def is_vip_time(vipTill):
    if time.time() < vipTill:
        return True
    else:
        return False