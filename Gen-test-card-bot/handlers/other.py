from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp
import json, string


# лямбда (если с строке есть слово старт то проверяем его и запускаем функцию)
@dp.message_handler(lambda message: 'старт' in message.text)
async def lambda_text(message: types.Message):
    await message.answer('старт')


# распарсиваем введенный текст через лямбду
@dp.message_handler(lambda message: message.text.startswith('финиш'))
async def lambda_text2(message: types.Message):
    await message.answer(message.text[6:])


# распарсиваем введенный текст через Text
@dp.message_handler(Text(equals='filter text', ignore_case=True))
async def filter_text(message: types.Message):
    await message.answer('filter text found')


# @dp.message_handler() # пустой хэндлер должен располагаться последним
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('censure.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()


# test
# @dp.message_handler()
# async def echo_send(message: types.Message):
#     if message.text.lower() == 'test':
#         await message.answer('passed')

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
