# машина состояний
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from database import sqlite3_db
from database.sqlite3_db import sql_add_command
from keyboards import admin_kb  # импортируем клавиатуру для админа
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Проверяем является ли пользователь администратором/модератором группы
# Получаем ID текущего пользователя
# Сообщение /moderator необходимо отправлять в группу!!!
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def admin_make_changes(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что пожелаете?',
                           reply_markup=admin_kb.kb_admin)  # выводим админскую панель если пользоватеь является модератором
    await message.delete()
    # await bot.delete_message()


# Начало диалога загрузхки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None) # коментируем так как ниже мы добавили отдельно хэндлеры
async def cm_start(message: types.Message):
    if message.from_user.id == ID:  # добавляем проверки на каждую команду, админ ли это или нет
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

    # await FSMAdmin.photo.set()
    # await message.reply('Загрузи фото')


# Выходим из машины состоний
# Размещаем после FSMAdmin.photo.set() так как инача не работает отмена, если пройти далее первого шага
# @dp.message_handler(state='*', commands='Отмена')
# @dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


# Начинаем ловить ответы и записываем их в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id  # по каждой картинке будет свой уникальный id
    await FSMAdmin.next()
    await message.reply('Введите название')


# Ловим ответ на 'Введите название'
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание')


# Ловим ответ на 'Введите описание'
# @dp.message_handler(state=FSMAdmin.name)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Укажите цену')


# Ловим ответ на 'Укажите цену'
# @dp.message_handler(state=FSMAdmin.name)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    """
    async with state.proxy() as data:
        await message.reply(str(data))  # выводим что записал пользователь в телеграм
    """

    await sql_add_command(state)  # обращаемся к базе данных для записи, await так как функция async

    await state.finish()  # бот выходит из машины состояний


# добавляем функционал для удаления данных из базы данных дял администратора
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite3_db.sql_delete_comand(callback_query.data.replace('del ', ''))
    # await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)
    await bot.answer_callback_query(callback_query.id, text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)

@dp.message_handler(commands='удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read_all = sqlite3_db.sql_read_all()
        for ret in read_all:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup()
                                   .add(InlineKeyboardButton(f'Удалить {ret[1]}',
                                                             callback_data=f'del {ret[1]}')))  # в базу возвращаем callback_data=f'del {ret[1]}'


# записываем команды для передачи хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(admin_make_changes, commands=['moderator'], is_chat_admin=True)
