import time
import logging
from create import db, bot
from mailing import messages
from utils import vip_status
from mailing import messages_operations
mailing = db.mailingToVip
users = db.users

async def send_vip_msg(userId, msg):
    try:
        cur_time = time.time()
        if msg['state'] == 'toVip1Day':
            cur_time += 24 * 60 * 60
        else:
            cur_time += 3 * 24 * 60 * 60
        res = await users.find_one({'id': userId})
        print(cur_time)
        if res['vipTill'] is None:
            return 0
        if res['vipTill'] > cur_time:
            return 0
        else:
            return await messages_operations.send_msg(userId, msg)
    except Exception as e:
        logging.error(e)
        return 2


