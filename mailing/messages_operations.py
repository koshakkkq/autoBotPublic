import time
import logging
from create import db, bot
from mailing.messages import msgs
from utils import vip_status
from aiogram import types
from keyboards.mailing import boards
mailing = db.mailing

async def add_msg(userId, msgName):
    try:
        if msgs[msgName] is None:
            return False
        cur_time = time.time()
        message = msgs[msgName]
        if callable(message['text']):
            res = await bot.get_chat(userId)
            message['text'] = message['text'](res.first_name)
        mailingTime = int(cur_time + message['delay'])
        add = {'userId': userId, 'text': message['text'], 'mailingTime': mailingTime,
               'photo': message['photo'], 'video': message['video'], 'toVip':message['toVip'],
               'state': message['state'], 'nextMsg': message['nextMsg'], 'keyboard': message['keyboard']}
        await mailing.insert_one(add)
        return True
    except Exception as e:
        logging.error(e)
        return False

async def add_msg_by_obj(userId, message):
    cur_time = time.time()
    mailingTime = int(cur_time + message['delay'])
    add = {'userId': userId, 'text': message['text'], 'mailingTime': mailingTime,
           'photo': message['photo'], 'video': message['video'], 'toVip': message['toVip'],
           'state': message['state'], 'nextMsg': message['nextMsg'], 'keyboard': message['keyboard']}
    await mailing.insert_one(add)
    return True

async def send_msg(userId, msg):
    try:
        isVip = await vip_status.is_vip(userId)
        if isVip == True and  msg['state'] == 'notVip':
            return 0
        if isVip == False and msg['state'] == 'vip':
            return 0
        if msg['photo'] is not None:
            photo = types.InputFile(msg['photo'])
            await bot.send_photo(chat_id=userId, photo=photo, caption=msg['text'], parse_mode=types.ParseMode.HTML, reply_markup=boards[msg['keyboard']])
        elif msg['video'] is not None:
            video = types.InputFile(msg['video'])
            await bot.send_video(chat_id=userId, video=video, caption=msg['text'], parse_mode=types.ParseMode.HTML, reply_markup=boards[msg['keyboard']])
        else:
            await bot.send_message(chat_id=userId, text=msg['text'],parse_mode=types.ParseMode.HTML, reply_markup=boards[msg['keyboard']])
        return 1
    except Exception as e:
        logging.error(e)
        return 2
