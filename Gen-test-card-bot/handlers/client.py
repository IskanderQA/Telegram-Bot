from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import dp, bot  # импортируем уже созданные экземпляры
from keyboards import kb_client  # импортируем пакет с лавиатурой
from cardgen import Card_Generator
from database import sqlite3_db


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Привет, я ваш помошник в генерации тестовых данных',
                               reply_markup=kb_client)  # reply_markup=kb_client
        await message.delete()
    except:
        await message.reply('Общение с ботом через личные сообщения, напишити ему: \nhttps://t.me/SimpleTestDataGenbot')


# @dp.message_handler(commands=['Сгенерировать_карту'])
async def gen_card(message: types.Message):
    await message.delete()
    await message.answer('Сгенерировал карту для оплаты в тестинге ' + Card_Generator.generate_pan())


# @dp.message_handler(commands=['Тестовые_CVV'])
async def help(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, """
    Успешная оплата - 123
    На карте недостаточно средств - 129
    Ошибка платежной системы - 208
    Оплата не более 5 рублей - 321
    Оплата только первый платеж - 325
     """)


# Выыодим в телеграм описание того что было загружено в БД
# @dp.message_handler(commands=['Показать_сгенерированные_карты'])
async def show_card_from_db(message: types.Message):
    await sqlite3_db.sql_read(message)


"""Голосовалка"""

# инлайн кнопки / inline
inlinekb = InlineKeyboardMarkup(row_width=2)
inline_buttons = [InlineKeyboardButton(text='Like', callback_data='like_1'),
                  InlineKeyboardButton(text='Dislike', callback_data='dislike_-1'),
                  InlineKeyboardButton(text='Result', callback_data='result')]
inlinekb.row(*inline_buttons)


@dp.message_handler(commands='vote')
async def vote_command(message: types.Message):
    await message.answer('Vote', reply_markup=inlinekb)


"""
@dp.callback_query_handler(text='like')
async def like_call(callback: types.CallbackQuery):
    await callback.message.answer('Vote: Like')
    await callback.answer('You\'r voted')
    # await callback.answer('You\'r voted', show_alert=True)
"""

answ = dict()


# можем обрабатывать несколько коллбэк кнопок в одном хэндлере
@dp.callback_query_handler(Text(contains='like_'))
async def like_callback(callback: types.CallbackQuery):
    result = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = result
        await callback.answer('You\'r vote')
    else:
        await callback.answer('You\'r allready vote', show_alert=True)


@dp.callback_query_handler(text='result')
async def like_result(callback: types.CallbackQuery):
    await callback.message.answer(answ)
    # await callback.answer('You\'r voted', show_alert=True)


"""Голосовалка"""


# записываем команды для передачи хендлеров
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(gen_card, commands=['Сгенерировать_карту'])
    dp.register_message_handler(help, commands=['Тестовые_CVV'])
    dp.register_message_handler(show_card_from_db, commands=['Показать_сгенерированные_карты'])
