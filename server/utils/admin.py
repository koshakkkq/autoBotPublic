import logging

import motor.motor_asyncio
from create import db
import time
from datetime import datetime

cities = db.cities
categories = db.categories
partners = db.partners


async def add_citie(name):
    try:
        await cities.update_one({'name': name}, {'$set': {'name': name}}, upsert=True)
        return True
    except Exception as e:
        logging.error(e)
        return False


async def add_category(city, name):
    try:
        await categories.insert_one({'name':name, 'city':city})
        return True
    except Exception as e:
        logging.error(e)
        return False


async def delete_city(cityName):
    try:
        await categories.delete_many({'city':cityName})
        await cities.delete_many({'city':cityName})
        await cities.delete_many({'name':cityName})
        return True
    except Exception as e:
        logging.error(e)
        return False

async def delete_category(cityName, categoryName):
    try:
        await partners.delete_many({'city':cityName, 'category':categoryName})
        await categories.delete_many({'name':categoryName})
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
        await partners.delete_many({'city': city, 'category': category, 'name':name})
        return True
    except Exception as e:
        logging.error(e)
        return False