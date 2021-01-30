#do not touch anything!
import aiogram
from aiogram import types
import logging as log
from config import FEEDBACK_USER_ID
from connection import bot, database_query
from config import ANSWER_TO_USER as text_to_user
from config import notallowed,block,ban
import sqlite3


async def feedback_message(message: types.Message):
    #this is for debug mode, if you need all info about user to be printed, uncomment it
    #log.info(f'Message ({message.content_type}) from {message.from_user.first_name} ({message.from_user.id}) with text: {message.text}')

    try:
        if message.chat.id == FEEDBACK_USER_ID:
            if message.reply_to_message is None:
                log.info(f"Активність в чаті адмінів")
            else:
                try:
                    units = database_query(f"SELECT user_id FROM messages WHERE message_id = {message.reply_to_message.message_id}")
                    unit = units[0][0]
                    if message.content_type == "text":
                        await bot.send_message(unit, message.text)
                    elif message.content_type == "photo":
                        capt = message.caption
                        await bot.send_photo(unit, message.photo[-1].file_id,caption=capt)
                    elif message.content_type == "video":
                        capt = message.caption
                        await bot.send_video(unit, message.video.file_id,caption=capt)
                    elif message.content_type == "sticker":
                        await bot.send_sticker(unit, message.sticker.file_id)
                    elif message.content_type == "audio":
                        capt = message.caption
                        await bot.send_audio(unit, message.audio.file_id,caption=capt)
                    elif message.content_type == "voice":
                        capt = message.caption
                        await bot.send_voice(unit, message.voice.file_id,caption=capt)
                    elif message.content_type == "document":
                        capt = message.caption
                        await bot.send_document(unit, message.document.file_id,caption=capt)
                    elif message.content_type == "location":
                        await bot.send_location(unit, message.location)
                    elif message.content_type == "animation":
                        capt = message.caption
                        await bot.send_animation(unit, message.animation.file_id,caption=capt)
                    elif message.content_type == "contact":
                        await bot.send_contact(unit, message.contact.file_id)
                except aiogram.utils.exceptions.BotBlocked:
                    await bot.send_message(message.chat.id,block)
        else:
            if message.forward_from == None:
                units = database_query(f"SELECT user_id FROM blocked WHERE user_id = {message.from_user.id}")
                unit = units
                #print(unit)
                if not unit:
                    forward_message_result = await bot.forward_message(FEEDBACK_USER_ID, message.chat.id, message.message_id)
                    database_query(f"INSERT OR IGNORE INTO messages(user_id,first_name,message_id,message) "
                                   f"VALUES('{message.from_user.id}','{message.from_user.first_name}','{forward_message_result.message_id}','{message.text}')")
                    await bot.send_message(message.chat.id, text_to_user)
                elif unit:
                    await bot.send_message(message.chat.id, ban)
            else:
                await message.answer(notallowed)
    except Exception as e:
        await message.answer(message.chat.id,f"{str(e)}")