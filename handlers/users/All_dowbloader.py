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


@dp.message_handler()
async def cmd_answer(message: types.Message):
    if message.text.startswith('https://youtube.be/') or message.text.startswith(
            'https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
        url = message.text
        yt = YouTube(url)
        title = yt.title
        author = yt.author
        channel = yt.channel_url
        resolution = yt.streams.get_highest_resolution().resolution
        file_size = yt.streams.get_highest_resolution().filesize
        length = yt.length
        date_published = yt.publish_date.strftime("%Y-%m-%d")
        views = yt.views
        picture = yt.thumbnail_url

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="yuklash", callback_data="download"))
   
        await message.answer_photo(f'{picture}', caption=f"📹 <b>{title}</b> <a href='{url}'>→</a> \n"
                                                         f"👤 <b>{author}</b> <a href='{channel}'>→</a> \n"
                                                   ,
                                   parse_mode='HTML', reply_markup=keyboard)  # Views#
    else:
        await message.answer(f"❗️<b>yuklab bo'lmadi!</b>", parse_mode='HTML')


@dp.callback_query_handler(text="download")
async def button_download(call: types.CallbackQuery):
    url = call.message.html_text
    yt = YouTube(url)
    title = yt.title
    author = yt.author
    resolution = yt.streams.get_highest_resolution().resolution
    stream = yt.streams.filter(progressive=True, file_extension="mp4")
    stream.get_highest_resolution().download(f'{call.message.chat.id}', f'{call.message.chat.id}_{yt.title}')
    with open(f"{call.message.chat.id}/{call.message.chat.id}_{yt.title}", 'rb') as video:
        await message.answer(f"❗️<b>Yulanmoqdaa...</b>", parse_mode='HTML')
        await bot.send_video(call.message.chat.id, video, caption=f"📹 <b>{title}</b> \n"  # Title#
                                                                  f"👤 <b>{author}</b> \n\n",  # Author Of Channel#
                             parse_mode='HTML')
        os.remove(f"{call.message.chat.id}/{call.message.chat.id}_{yt.title}")




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






