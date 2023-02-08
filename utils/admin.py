import asyncio
import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime
from bson.objectid import ObjectId
from create import bot
from utils.vip_status import  add_balance

users = db.users
cities = db.cities
categories = db.categories
partners = db.partners
categories_tags = db.categories_tags
withdrawal = db.withdrawal

async def add_citie(name):
    try:
        await cities.update_one({'name': name}, {'$set': {'name': name}}, upsert=True)
        return True
    except Exception as e:
        logging.error(e)
        return False


async def add_category(city, name):
    try:
        res = await categories.insert_one({'name':name, 'city':city})
        await categories_tags.insert_one({'name':name, 'city':city, 'categoryId':str(res.inserted_id), 'categoryName':name})
        return True
    except Exception as e:
        logging.error(e)
        return False



async def delete_city(cityId):
    try:
        await categories.delete_many({'city':cityId})
        await partners.delete_many({'city':cityId})
        await cities.delete_many({'_id':ObjectId(cityId)})
        return True
    except Exception as e:
        logging.error(e)
        return False

async def delete_category(cityId, categoryId):
    try:
        await partners.delete_many({'city':cityId, 'category':categoryId})
        await categories.delete_many({'_id':ObjectId(categoryId)})
        return True
    except Exception as e:
        logging.error(e)
        return False


async def add_partner(city, category, text, photo, name):
    try:
        res = await partners.insert_one({'city': city, 'category': category, 'text':text, 'photo':photo, 'name':name})
        return True
    except Exception as e:
        logging.error(e)
        return False

async def delete_partner(city, category, name):
    try:
        await partners.delete_many({'city': city, 'category': category, '_id':ObjectId(name)})
        return True
    except Exception as e:
        logging.error(e)
        return False


async def add_category_tag(city, categoryId, name, categoryName):
    try:
        await categories_tags.insert_one(
            {'name': name, 'city': city, 'categoryId': categoryId, 'categoryName': categoryName})
        return True
    except Exception as e:
        logging.error(e)
        return False


async def mailing_admin(msg, vip):
    res = None
    if vip == False:
        res = users.find({'vipTill':{'$lt':time.time()}})
    else:
        res = users.find({'vipTill':{'$gte':time.time()}})
    for document in await res.to_list(length=1000000):
        try:
            await bot.send_message(chat_id=document['id'], text=msg)
            await asyncio.sleep(0.07)
        except Exception as e:
            logging.error(e)
            continue


async def add_withdrawal(sum, id):
    print(sum)
    if sum < 100:
        return False, 0
    try:
        res = await users.find_one({'id':id})
        if res['balance'] < sum:
            return False, 1
        await withdrawal.insert_one(
            {'sum': sum, 'id':id})
        await users.update_one({'id':id},{'$inc':{'balance':-sum}})
        return True, 0
    except Exception as e:
        logging.error(e)
        return False, 2


async def get_withdrawal_card():
    try:
        res = await withdrawal.find_one({})
        return res, True
    except Exception as e:
        logging.error(e)
        return None, False

async def reload_withdrawal(id):
    try:
        res = await withdrawal.find_one({'id':id})
        await withdrawal.delete_one({'id':id})
        await withdrawal.insert_one({'id':id, 'sum':res['sum']})
        return True
    except Exception as e:
        logging.error(e)
        return None


async def accept_withdrawal(withdrawalId):
    try:
        await withdrawal.delete_one({'_id': ObjectId(withdrawalId)})
        return True
    except Exception as e:
        logging.error(e)
        return None


async def reject_withdrawal(withdrawalId):
    try:
        res = await withdrawal.find_one({'_id': ObjectId(withdrawalId)})
        await withdrawal.delete_one({'_id': ObjectId(withdrawalId)})
        balance_result = await add_balance(res['id'], res['sum'])
        if balance_result == False:
            return False
        return True
    except Exception as e:
        logging.error(e)
        return None