from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # позволяет хранить данные в оперативной памяти

storage = MemoryStorage()  # иницилизируем место хранения информации

# bot = Bot(token='2055868218:AAEA55qK9t9Xs2soV9YGVjY6f7rHrSqcyGI') # @simpletestdatagenbot on heroku
bot = Bot(token='2099135297:AAEJN4KELCd6uWaLvA_wzU0tdGl2CHagSiE')  # @simpletestdatagentestbot
dp = Dispatcher(bot, storage=storage)
