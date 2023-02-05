import asyncio
import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime
from bson.objectid import ObjectId
from create import bot


users = db.users
cities = db.cities
categories = db.categories
partners = db.partners
categories_tags = db.categories_tags

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
        print(res.inserted_id)
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