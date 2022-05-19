from aiogram import executor
from create_bot import dp
from database import sqlite3_db

async def on_startup(_):
    print('On-air')
    sqlite3_db.sql_start()


# импортируем handlers
from handlers import client, admin, other

# импортируем хэндлеры которые мы регистрируем отдельно
admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)  # должен быть последним так как есть пустой хэнлер в other

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
