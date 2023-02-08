
import logging

from aiogram import executor
from create import dp, db
from utils import vip_status
from mailing import proceed



import asyncio

logging.basicConfig(level=logging.ERROR,
                    filename='log.txt',
                    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%Y-%m-%d:%H:%M:%S')



from handlers import hello, vip, mailing, pay

hello.register_handlers_client(dp)
vip.register_handlers_client(dp)
mailing.register_handlers_client(dp)
pay.register_handlers_client(dp)
async def on_startup(dp):
    asyncio.create_task(proceed.scheduler())

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

