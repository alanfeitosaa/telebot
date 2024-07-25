from pyrogram import Client, filters
from os import getenv, environ
from dotenv import load_dotenv
import asyncio
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from datetime import datetime, timedelta
import configparser
import telebot
import sqlite3
import time
import json

load_dotenv()

app = Client(
    'cronos_bot',
    api_id=getenv('TELEGRAM_API_ID'),
    api_hash=getenv('TELEGRAM_API_HASH'),
    bot_token=getenv('TELEGRAM_BOT_TOKEN_CHRONOS')
)

# local = 'servidor'
local = 'casa'

config = configparser.ConfigParser()
config.optionxform = str
if local == 'servidor':
    config.read("/root/Bots/cfgbot.ini")
else:
    config.read("cfgbot.ini")

hostCaptura = getenv('HOST')
userBanco = getenv('USERBANCO')
passBanco = getenv('PASSBANCO')
urlDragon = getenv('URLDRAGONTIGER')
urlBacBo = getenv('URLBACBO')
urlFootball = getenv('URLFOOTBALL')
urlFutbol = getenv('URLFUTBOL')
token = getenv('TELEGRAM_BOT_TOKEN_CHRONOS_DEV')
chatDev = getenv('CHATDEV')
user_adm = [130763639, 1899597306, 5222727252]

user_list = user_adm
for i in config.get('clientes', 'clientesAtivos').split(','):
    user_list.append(int(i))

bot = telebot.TeleBot(token=token, parse_mode='MARKDOWN')


def deleteClientes():
    if local == 'servidor':
        con = sqlite3.connect('/root/Bots/master.db')
    else:
        con = sqlite3.connect('master.db')
    cur = con.cursor()
    cur.execute("""
DELETE FROM clientes;""")
    con.commit()
    con.close()


def insertCliente(chat_id):
    if local == 'servidor':
        con = sqlite3.connect('/root/Bots/master.db')
    else:
        con = sqlite3.connect('master.db')
    cur = con.cursor()
    cur.execute(f"""
INSERT INTO clientes (chat_id) VALUES ({chat_id});
""")
    con.commit()
    con.close()


def selectCliente():
    if local == 'servidor':
        con = sqlite3.connect('/root/Bots/master.db')
    else:
        con = sqlite3.connect('master.db')
    cur = con.cursor()
    cur.execute("""
SELECT * FROM clientes;
""")
    clientes = []
    for i in cur.fetchall():
        clientes.append(int(i[0]))
    con.close()
    return clientes


deleteClientes()


@app.on_message(filters.user(user_list) & filters.command("start"))
async def start(client, message):
    await app.send_message(
        message.chat.id,
        f'🤖 Olá **{message.chat.first_name}**!\n🔢 Escolha uma das opções de sinais abaixo!',
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Bac Bo"]
                # ["Dragon Tiger"],
                # ["Football Studio"],
                # ["Futbol Studio"]
            ],
            resize_keyboard=True
        )
    )


@app.on_message(filters.user(user_list) & filters.command('help'))
async def help(client, message):
    print(message.chat.id, message.chat.username, message.chat.first_name, message.text)
    await message.reply(
        f'Olá **{message.chat.first_name}**! Em que posso ajudá-lo?',
        reply_to_message_id=message.id
    )


@app.on_message(filters.user(user_list) & filters.text & filters.regex(r'Bac Bo'))
async def conserv(client, message):
    if message.chat.id not in selectCliente():
        horario = time.strftime('%H:%M')
        if '03:50' >= horario or '04:00' <= horario:
            await app.send_message(
                message.chat.id,
                f'🤖 Olá **{message.chat.first_name}**!\nNo momento o servidor está em processo de reinício. Aguarde para solicitar sinal após 00:10hrs'
            )
        else:
            insertCliente(message.chat.id)
            if local == 'servidor':
                cmd = f"python3 /root/Bots/BacBo_VIP.py {str(message.chat.id)} {str(message.chat.first_name)}"
            else:
                cmd = f"python BacBo_VIP.py {str(message.chat.id)} {str(message.chat.first_name)}"
            await asyncio.create_subprocess_shell(cmd)


# @app.on_message(filters.user(user_list) & filters.text & filters.regex(r'Dragon Tiger'))
# async def conserv(client, message):
#     if message.chat.id not in selectCliente():
#         insertCliente(message.chat.id)
#         horario = time.strftime('%H:%M')
#         if '00:10' >= horario or '23:50' <= horario:
#             await app.send_message(
#                 message.chat.id,
#                 f'🤖 Olá **{message.chat.first_name}**!\nNo momento o servidor está em processo de reinício. Aguarde para solicitar sinal após 00:10hrs'
#             )
#         else:
#             if local == 'servidor':
#                 cmd = f"python3 /root/Bots/DragonTiger_VIP.py {str(message.chat.id)} {str(message.chat.first_name)}"
#             else:
#                 cmd = f"python controle.py {str(message.chat.id)} {str('Não')} {str('Dragon')} {str(message.chat.first_name)}"
#             await asyncio.create_subprocess_shell(cmd)
#
#
# @app.on_message(filters.user(user_list) & filters.text & filters.regex(r'Football Studio'))
# async def conserv(client, message):
#     if message.chat.id not in selectCliente():
#         insertCliente(message.chat.id)
#         horario = time.strftime('%H:%M')
#         if '00:10' >= horario or '23:50' <= horario:
#             await app.send_message(
#                 message.chat.id,
#                 f'🤖 Olá **{message.chat.first_name}**!\nNo momento o servidor está em processo de reinício. Aguarde para solicitar sinal após 00:10hrs'
#             )
#         else:
#             if local == 'servidor':
#                 cmd = f"python3 /root/Bots/controle.py {str(message.chat.id)} {str('Não')} {str('Football')} {str(message.chat.first_name)}"
#             else:
#                 cmd = f"python controle.py {str(message.chat.id)} {str('Não')} {str('Football')} {str(message.chat.first_name)}"
#             await asyncio.create_subprocess_shell(cmd)
#
#
# @app.on_message(filters.user(user_list) & filters.text & filters.regex(r'Futbol Studio'))
# async def conserv(client, message):
#     if message.chat.id not in selectCliente():
#         insertCliente(message.chat.id)
#         horario = time.strftime('%H:%M')
#         if '00:10' >= horario or '23:50' <= horario:
#             await app.send_message(
#                 message.chat.id,
#                 f'🤖 Olá **{message.chat.first_name}**!\nNo momento o servidor está em processo de reinício. Aguarde para solicitar sinal após 00:10hrs'
#             )
#         else:
#             if local == 'servidor':
#                 cmd = f"python3 /root/Bots/controle.py {str(message.chat.id)} {str('Não')} {str('Futbol')} {str(message.chat.first_name)}"
#             else:
#                 cmd = f"python controle.py {str(message.chat.id)} {str('Não')} {str('Futbol')} {str(message.chat.first_name)}"
#             await asyncio.create_subprocess_shell(cmd)
#             await asyncio.create_subprocess_shell(cmd)
#
#
# @app.on_message(filters.user(user_adm) & filters.text & filters.regex(r'autoRollet...'))
# async def conserv(client, message):
#     try:
#         qtdJogadas = str(message.text[-3:])
#         user = str(message.chat.id)
#         dados = {str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")): user+","+qtdJogadas}
#         if local == 'servidor':
#             with open("/root/Bots/sampleAutoRollet.json", "w") as out:
#                 json.dump(dados, out)
#         else:
#             with open("sampleAutoRollet.json", "w") as out:
#                 json.dump(dados, out)
#     except ValueError:
#         await app.send_message(
#             message.chat.id,
#             f'O formato escolhido está errado, utilize como nos exemplos (**autoRollet080** para 80 casas ou **autoRollet320** para 320 casas)'
#         )
        
app.run()
