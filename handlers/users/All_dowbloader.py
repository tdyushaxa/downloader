import io
import logging
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


@dp.message_handler(Text(startswith="https://youtu"))
async def Yuotube_downloader(message:types.Message):
    link=message.text
    buffer=io.BytesIO()
    downl = YouTube(link).streams.get_by_itag(itag=18)
    downl.stream_to_buffer(buffer=buffer)
    buffer.seek(0)
    file_name=downl.title
    await message.answer(f'{message.from_user.full_name} video yuklanmoqda...')
    await message.answer_video(video=buffer,caption=file_name)


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






