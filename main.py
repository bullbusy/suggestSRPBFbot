#do not touch anything!
import asyncio
from aiogram import types
import logging as log
from feedback import feedback_message
from connection import dispatcher, database_try_create
from connection import database_query
from config import *
from connection import bot
async def main():
    log.basicConfig(level=log.INFO)
    log.info("Bot started successfully")
    database_try_create()
    await dispatcher.start_polling()


@dispatcher.message_handler(commands=['start'])
async def welcome_message_event(message: types.Message):
    await message.answer(f"Привіт!\nНапиши, що тебе цікавить і ми скоро надамо відповідь")
@dispatcher.message_handler(commands=['ban'])
async def banning(message: types.Message):
    if message.chat.id == FEEDBACK_USER_ID:
        units = database_query(f"SELECT user_id FROM messages WHERE message_id = {message.reply_to_message.message_id}")
        unit = units[0][0]
        some = database_query(f"SELECT user_id FROM blocked WHERE user_id = {unit}")
        resu = some
        #print(resu)
        if not resu:
            database_query(f"INSERT INTO blocked(user_id) "
                           f"VALUES('{unit}')")
            await message.answer(f"Було заблоковано {str(unit)}")
            await bot.send_message(unit,"Ви були заблоковані")
@dispatcher.message_handler(commands=['unban'])
async def banning(message: types.Message):
    if message.chat.id == FEEDBACK_USER_ID:
        units = database_query(f"SELECT user_id FROM messages WHERE message_id = {message.reply_to_message.message_id}")
        unit = units[0][0]
        some = database_query(f"SELECT user_id FROM blocked WHERE user_id = {unit}")
        resu = some
        #print(resu[0][0])
        if resu:
            try:
                database_query(f"DELETE FROM blocked WHERE user_id = {resu[0][0]}")
                await message.answer(f"Було розблоковано {str(resu[0][0])}")
                await bot.send_message(unit,"Ви були розблоковані")
            except Exception as e:
                print(str(e))

@dispatcher.message_handler(lambda message: True, content_types=['text', 'photo', 'sticker', 'video', 'audio', 'voice', 'location', 'animation', 'contact', 'document'])
async def feedback_message_event(message: types.Message):
    await feedback_message(message)


if __name__ == '__main__':
    asyncio.run(main())

