import io
import logging
import os

from aiogram import types
from aiogram.dispatcher.filters import Text
from pytube import YouTube

from handlers.users.downlader_tiktok import download_tiktok
from handlers.users.insta_download import insta_download
from loader import dp

@dp.message_handler(Text(startswith='https://vt.tiktok.com'))
async def downloader(message:types.Message):
    link=message.text
    lookup=download_tiktok(link)
    if lookup == 'Bad':
        await message.answer('bu link orqali hech nima topilmadi')
    else:
        await message.answer(f'{message.from_user.full_name} video yuklanmoqda...')
        await message.answer_video(lookup['video'])
        await message.delete()
        await message.answer(lookup['title'])


@dp.message_handler(Text(startswith='https://youtu'))
async def cmd_answer(message: types.Message):
    url = message.text
    yt = YouTube(url)
    title = yt.title
    author = yt.author
    resolution = yt.streams.get_highest_resolution().resolution
    stream = yt.streams.filter(progressive=True, file_extension="mp4")
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{yt.title}')
    with open(f"{message.chat.id}/{message.chat.id}_{yt.title}", 'rb') as video:
        await message.answer_video(message.chat.id, video, caption=f"📹 <b>{title}</b> \n"  # Title#
                                                                    f"👤 <b>{author}</b> \n\n",  # Author Of Channel#
                                parse_mode='HTML')
        os.remove(f"{message.chat.id}/{message.chat.id}_{yt.title}")




    




@dp.message_handler(Text(startswith="https://www.instagram.com"))
async def instagram_downloader(message:types.Message):
    link=message.text
    lookup=insta_download(link)
    if lookup['type']=='video':
        await message.answer(f"{message.from_user.full_name}  video yuklanmoqda...")
        await message.answer_video(lookup['video'])
    elif lookup['type']=='Carousel':
        for i in lookup['Carousel']:
            await message.answer(f'{message.from_user.full_name} video yuklanmoqda...')
            await message.answer_document(document=i)
    else:await message.answer('natija topilmadi')






