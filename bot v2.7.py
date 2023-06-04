from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
from bs4 import BeautifulSoup as BS

bot = Bot(token='your_token_here',
          parse_mode='HTML')
dp = Dispatcher(bot)

# Parser
r = requests.get('https://ngs42.ru/horoscope/daily/')
soup = BS(r.content, 'html.parser')
signs = soup.find_all('article', class_='IGRa5')

# Main Vars
with open('path_to\\about_signs.json',
          encoding='utf8') as f:
    data = json.load(f)

dict_horo = data['dict_horo']
zodiac_about = data['zodiac_about']
zodiac_horo = data['zodiac_horo']
dict_about = data['dict_about']
bot_text = data['bot_text']
zz = data['zz']
lst_horo = []
lst_about = []
horoscope = []

# Get Horoscope
for sign in signs:
    sign = sign.find('div', class_='BDPZt KUbeq')
    horoscope.append(sign)

# Signs Btns
for k, v in zodiac_horo.items():
    v = InlineKeyboardButton(k, callback_data=v)
    lst_horo.append(v)

for k, v in zodiac_about.items():
    v = InlineKeyboardButton(k, callback_data=v)
    lst_about.append(v)

# Inline Btns
back = InlineKeyboardButton('Назад', callback_data='back')
about_back = InlineKeyboardButton('Назад', callback_data='about_back')
btns = InlineKeyboardMarkup().add(*lst_horo)
sbtns = InlineKeyboardMarkup().add(*lst_about)
back_btn = InlineKeyboardMarkup().add(back)
about_back_btn = InlineKeyboardMarkup().add(about_back)

# Keyboard Btns
horo_btn = KeyboardButton('Гороскоп')
sign_btn = KeyboardButton('О знаке')
mb = ReplyKeyboardMarkup(resize_keyboard=True).add(horo_btn, sign_btn)


# /start /help
def commands(name, i):
    @dp.message_handler(commands=[name])
    async def command(msg: types.Message):
        await msg.answer(f'Привет, {msg.from_user.full_name}!{bot_text[i]}',
                         reply_markup=mb)

commands('start', 0)
commands('help', 1)


# /text
@dp.message_handler(content_types=['text'])
async def text(msg: types.Message):
    if msg.text.lower() == 'привет':
        await msg.answer(f'Привет, {msg.from_user.full_name}!{bot_text[2]}',
                         reply_markup=btns)
    elif msg.text.lower() == 'гороскоп':
        await msg.answer(f'{bot_text[3]}', reply_markup=btns)
    elif msg.text.lower() == 'о знаке':
        await msg.answer(f'{bot_text[4]}', reply_markup=sbtns)
    else:
        await msg.answer(f'Ой, {msg.from_user.full_name},{bot_text[5]}',
                         reply_markup=mb)


# Horoscope
def send_horo(name, i):
    @dp.callback_query_handler(lambda x: x.data == name)
    async def reaction(call: types.callback_query):
        await bot.answer_callback_query(call.id)
        await bot.send_message(call.message.chat.id,
                               zz[i] + horoscope[i].text,
                               reply_markup=back_btn)

for k, v in dict_horo.items():
    send_horo(k, v)


# About Signs
def send_about(name, i):
    @dp.callback_query_handler(lambda x: x.data == name)
    async def reaction(call: types.callback_query):
        await bot.answer_callback_query(call.id)
        await bot.send_message(call.message.chat.id,
                               dict_about[i],
                               reply_markup=about_back_btn)

for k, v in dict_about.items():
    send_about(k, k)


# Back Btn
def back(name, i, markup):
    @dp.callback_query_handler(lambda x: x.data == name)
    async def reaction(call: types.callback_query):
        await bot.answer_callback_query(call.id)
        await bot.send_message(call.message.chat.id,
                               f'{bot_text[i]}',
                               reply_markup=markup)

back('back', 6, btns)
back('about_back', 7, sbtns)

executor.start_polling(dp, skip_updates=True)
