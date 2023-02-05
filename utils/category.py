import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime
from bson.objectid import ObjectId
from collections import defaultdict



cities = db.cities
categories = db.categories
partners = db.partners
categories_tags = db.categories_tags


async def get_cities(skipped):
    try:
        cursor = cities.find({}).sort('name')
        cur = 0
        docs = []
        for document in await cursor.to_list(length=100):
            if skipped != 0:
                skipped-=1
                continue
            docs.append({'name':document['name'], 'id':str(document['_id'])})
            cur+=1
            if cur == 3:
                break
        return True, docs
    except Exception as e:
        logging.error(e)
        return False, None

async def get_city_name_by_id(id):
    try:
        cursor = await cities.find_one({'_id':ObjectId(id)})
        return cursor['name']
    except Exception as e:
        logging.error(e)
        return None


async def get_category_by_id(id):
    try:
        cursor =await categories.find_one({'_id': ObjectId(id)})
        return cursor['name']
    except Exception as e:
        logging.error(e)
        return None


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
            docs.append({'name':document['name'], 'id':str(document['_id'])})
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
            docs.append({'id':str(document['_id']), 'name':document['name'] })
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



async def get_partner_info(cityName, categoryName, partnerId):
    try:
        res = await partners.find_one({'city': cityName, 'category': categoryName, '_id':ObjectId(partnerId)})
        return res
    except Exception as e:
        logging.error(e)
        return False, None

async def get_categories_by_search_old(skipped, city, req):
    try:
        cursor = categories.find({'$text':{'$search':req}, 'city':city}, { 'score': { '$meta': "textScore" } }).sort( 'score')
        cur = 0
        docs = []
        for document in await cursor.to_list(length=100):
            if skipped != 0:
                skipped -= 1
                continue
            docs.append({'name':document['name'], 'id':str(document['_id'])})
            cur += 1
            if cur == 6:
                break
        return True, docs

    except Exception as e:
        logging.error(e)
        return False, None

async def get_categories_by_search(skipped, city, req):
    try:
        cursor = categories_tags.find({'$text':{'$search': req},'city':city}, {'score':{'$meta':'textScore'}} ).sort('score')
        was = defaultdict(int)
        cur = 0
        docs = []
        for document in await cursor.to_list(length = 100000):
            if was[document['categoryId']] != 0:
                continue
            if skipped != 0:
                was[document['categoryId']] = 1
                skipped -= 1
                continue

            docs.append({'name': document['categoryName'], 'id': document['categoryId']})
            was[document['categoryId']] = 1
            cur += 1
            if cur == 6:
                break
        return True, docs
    except Exception as e:
        logging.error(e)
        return False, None


async def get_categories_by_search_count(city, req):
    try:
        cnt = await categories_tags.count_documents({'$text':{'$search': req},'city':city})
        return True, cnt

    except Exception as e:
        logging.error(e)
        return False, 0