
import logging

from aiogram import executor
from create import dp, db
from utils import vip_status

logging.basicConfig(level=logging.INFO, filename='log.txt', format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S')



from handlers import hello, vip

hello.register_handlers_client(dp)
vip.register_handlers_client(dp)



if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)

