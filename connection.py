#do not touch anything!

from aiogram import Bot, Dispatcher
import sqlite3 as sql
from config import TELEGRAM_TOKEN, DATABASE_PATH

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)


def database_try_create():
    database_query('''CREATE TABLE IF NOT EXISTS messages(
        user_id INTEGER,
        first_name VARCHAR,
        message_id INT,
        message VARCHAR)''')
    database_query('''CREATE TABLE IF NOT EXISTS blocked(
        user_id INTEGER)''')



def database_query(query: str):
    connect = sql.connect(DATABASE_PATH, check_same_thread=False)
    with connect:
        cursor = connect.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    if connect:
        connect.commit()
        connect.close()

    return result
