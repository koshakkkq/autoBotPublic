import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime

cities = db.cities
categories = db.categories
partners = db.partners


async def get_cities(skipped):
    try:
        cursor = cities.find({}).sort('name')
        cur = 0
        docs = []
        for document in await cursor.to_list(length=100):
            if skipped != 0:
                skipped-=1
                continue
            docs.append(document['name'])
            cur+=1
            if cur == 3:
                break
        return True, docs
    except Exception as e:
        logging.error(e)
        return False, None

async def get_cities_count():
    try:
        n = await cities.count_documents({})
        return True, n
    except Exception as e:
        logging.error(e)
        return False, None


async def get_categories(skipped, city):
    try:
        cursor = categories.find({'city':city}).sort('name')
        cur = 0
        docs = []
        for document in await cursor.to_list(length = 100):
            if skipped != 0:
                skipped -= 1
                continue
            docs.append(document['name'])
            cur += 1
            if cur == 6:
                break
        return True, docs
    except Exception as e:
        logging.error(e)
        return False, None


async def get_categories_count(city):
    try:
        n = await categories.count_documents({'city':city})
        return True, n
    except Exception as e:
        logging.error(e)
        return False, None


async def get_partners(skipped, city, category):
    try:
        cursor = partners.find({'city':city, 'category':category}).sort('name')
        cur = 0
        docs = []
        for document in await cursor.to_list(length = 100):
            if skipped != 0:
                skipped -= 1
                continue
            docs.append(document['name'])
            cur += 1
            if cur == 6:
                break
        return True, docs
    except Exception as e:
        logging.error(e)
        return False, None


async def get_partners_count(city, category):
    try:
        n = await categories.count_documents({'city':city, 'category':category})
        return True, n
    except Exception as e:
        logging.error(e)
        return False, None



async def get_partner_info(cityName, categoryName, partnerName):
    try:
        res = await partners.find_one({'city': cityName, 'category': categoryName, 'name':partnerName})
        return res
    except Exception as e:
        logging.error(e)
        return False, None