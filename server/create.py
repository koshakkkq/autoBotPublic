from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio
from utils import config_parser


config = config_parser.parse_config()

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

API_TOKEN = config['tg_token']

db = client.autoBot

adminId = config['adminId']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
