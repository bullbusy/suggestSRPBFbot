#do not touch anything!
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import BOT_TOKEN, FEEDBACK_USER_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome_message_event(message: types.Message):
    await message.answer(f"Привіт! 👋\nНапиши своє повідомлення та згодом ми відповімо.️")

@dp.message_handler(lambda message: True, content_types=['text', 'photo', 'sticker', 'video', 'audio', 'voice', 'location', 'animation', 'contact', 'document'])
async def feedback_message_event(message: types.Message):
    await feedback_message(message)

async def feedback_message(message: types.Message):

    try:
        if message.chat.id == FEEDBACK_USER_ID:
            if message.reply_to_message is None:
                await message.answer(f'To reply to the user, reply to the message sent from him')
            else:
                try:
                    if message.content_type == "text":
                        await bot.send_message(message.text)
                    elif message.content_type == "photo":
                        capt = message.caption
                        await bot.send_photo(message.photo[-1].file_id,caption=capt)
                    elif message.content_type == "video":
                        capt = message.caption
                        await bot.send_video(message.video.file_id,caption=capt)
                    elif message.content_type == "sticker":
                        await bot.send_sticker(message.sticker.file_id)
                    elif message.content_type == "audio":
                        capt = message.caption
                        await bot.send_audio(message.audio.file_id,caption=capt)
                    elif message.content_type == "voice":
                        capt = message.caption
                        await bot.send_voice(message.voice.file_id,caption=capt)
                    elif message.content_type == "document":
                        capt = message.caption
                        await bot.send_document(message.document.file_id,caption=capt)
                    elif message.content_type == "location":
                        await bot.send_location(message.location)
                    elif message.content_type == "animation":
                        capt = message.caption
                        await bot.send_animation(message.animation.file_id,caption=capt)
                    elif message.content_type == "contact":
                        await bot.send_contact(message.contact.file_id)
                except aiogram.utils.exceptions.BotBlocked:
                    await bot.send_message(message.chat.id)
    except Exception as e:
        await message.answer(message.chat.id,f"{str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp)