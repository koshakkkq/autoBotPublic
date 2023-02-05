import time
import logging
from create import db
import asyncio
import aioschedule
from mailing import to_vip, messages_operations
mailing = db.mailing
users = db.users
was_mailed = db.was_mailed
async def procceed_msg(res, err):
    if err:
        raise err



async def procced_msgs():
    try:
        cursor = mailing.find({'mailingTime':{'$lt':time.time()}})
        for document in await cursor.to_list(length=100000):
            res = 0
            if document['state'].startswith('toVip'):
                res = await to_vip.send_vip_msg(document['userId'], document)
            else:
                res = await messages_operations.send_msg(document['userId'], document)
                if res == 1:
                    await messages_operations.add_msg(document['userId'], document['nextMsg'])
            if res == 1:
                await asyncio.sleep(0.05)
        await mailing.delete_many({'mailingTime':{'$lt':time.time()}})
        await send_to_ended_vip()
    except Exception as e:
        logging.error(e)
        return False


async def send_to_ended_vip():
    try:
        cur_time = time.time()
        cur_time -= 22*60*60
        cursor = users.aggregate([{
        '$lookup':{
            'from' : 'was_mailed',
            'localField': 'id',
            'foreignField':'id',
            'as': 'result',
            }
        }, {
        '$match':{
            'result':{
                '$exists': True,
                '$eq': []
            },
            'vipTill':{
                '$lt': cur_time,
            }

        }}])
        for document in await cursor.to_list(length=100000):
            #todo раскоменить
            was_mailed.insert_one({'id':document['id']})
            await messages_operations.add_msg(document['id'], 'vipEnd1')
    except Exception as e:
        logging.error(e)
        return 2


async def scheduler():
    aioschedule.every(50).seconds.do(procced_msgs)
    while True:
        await asyncio.sleep(50)
        await aioschedule.run_pending()
