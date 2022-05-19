import sqlite3 as sqlite3
from create_bot import dp, bot


def sql_start():
    global base, cursor
    base = sqlite3.connect('simple_test_dgb.db')
    cursor = base.cursor()
    if base:
        print('DB connected OK')
    base.execute("""
        CREATE TABLE IF NOT EXISTS testing (
        photo TEXT,
        name TEXT PRIMARY KEY,
        description TEXT,
        price TEXT)
    """)
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO testing VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()


# чтение из базы данных (fetchall выгружает данные в виде списка)
async def sql_read(message):
    for ret in cursor.execute("SELECT * FROM testing").fetchall():
        print(ret)
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')


def sql_read_all():
    return cursor.execute("SELECT * FROM testing").fetchall()


def sql_delete_comand(data):
    cursor.execute("DELETE FROM testing WHERE name == ?", (data,))
    base.commit()
