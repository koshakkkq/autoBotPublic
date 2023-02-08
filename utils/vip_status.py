import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime
from mailing.messages_operations import add_msg, add_msg_by_obj
from mailing.messages import get_text_vipEnd1, get_text_vipEnd3
users = db.users



async def add_balance(id, val):
    try:
        await users.update_one({'id':id}, {'$inc':{'balance':val}})
        return True
    except Exception as e:
        logging.error(e)
        return False

#ПОМЕНЯТЬ
async def set_vip(id, days, name, addBonuses = True):
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
        #delay29Days = vipTill - 25 * 60 * 60 - 1
        delay29Days = 40
        msg = await get_text_vipEnd1(name, delay29Days)
        await add_msg_by_obj(id, msg)
        #delay27Days = vipTill - 3*24 * 60 * 60 - 60 * 60 - 1
        delay27Days = 20
        msg = await get_text_vipEnd3(name, delay27Days)
        await add_msg_by_obj(id, msg)
        if (addBonuses == True):
            await add_balance(document['ref'], 500*0.05)
            await add_balance(id, 500*0.05)
        return True
    except Exception as e:
        logging.error(e)
        return False

async def pay_by_bonuses(id, name):
    try:
        res = await users.find_one({'id':id})
        if res['balance'] < 500:
            return False, res['balance']
        await users.update_one({'id':id}, {'$inc':{'balance':-500}})
        res = await set_vip(id, 30, name, False)
        return True, 0
    except Exception as e:
        logging.error(e)
        return False, 0


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