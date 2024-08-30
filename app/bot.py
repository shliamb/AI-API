import logging

# logging.getLogger('aiogram').propagate = True # Блокировка логирование aiogram до его импорта
# logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл

from keys import (token_telegram)

# import time
# import sys
import re
import random
# import os
import asyncio
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F, Router
# from aiogram.enums import ParseMode
# from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# import csv
# import datetime
# from io import StringIO, BytesIO

from worker_db import get_user_by_id, get_user_by_username, update_user, adding_user

# from worker_db import ()


dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token_telegram) # Initialize Bot instance with a default parse mode which will be passed to all API calls



#########
# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')
    # await asyncio.sleep(5)

# Generation a Unique Username
async def gen_username(about):
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', about)
    username = cleaned_text + str(random.randint(1, 10))
    return username or None

########



#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    # Menu bot
    bot_commands = [
       BotCommand(command="/mykey", description="Show my key"),
       BotCommand(command="/balance", description="Balance"),
       BotCommand(command="/addmoney", description="Add money"),
       BotCommand(command="/getstat", description="Get my stats"),
       BotCommand(command="/instructions", description="API Instructions"),
    ]
    await bot.set_my_commands(bot_commands)


    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "User"))
    username = await gen_username(about) # Генерим уникальное имя из about, это важно, так как на нем завязанна проверка колличества попыток обращения и временная блокировка

    is_on_user = await get_user_by_id(id) # Получаем по ID данные из базы

    if is_on_user is not None:
        await message.answer("You are already registered in the system!") # Уже есть

    if is_on_user is None:

        while True: # Сразу проверяю на уникальность в базе Username, если не уникально, то генерим по новой, пока не попадем на уникальный вариант
            data_by_username = await get_user_by_username(username)
            if data_by_username is not None:
                username = await gen_username(about) # Генерим заново
            else:
                break
        
        if data_by_username is None: # Зачем то перепроверяю, хз
            user_data = {
                            "id": id,
                            "name": name,
                            "full_name": full_name,
                            "first_name":first_name,
                            "last_name": last_name,
                            "username": username
                        }

            await adding_user(user_data)

            is_on_user = await get_user_by_id(id)

            text_get_key = (  
                            "Use the following keys to use the API:\n\n"
                            "<b>Username:</b>\n"
                            f"Username: <code>{is_on_user.username}</code>\n"
                            "Add to: <i>Json</i>\n"
                            "\n"
                            "<b>API Key:</b>\n"
                            "Key: <code>appkey</code>\n"
                            f"Value: <code>{is_on_user.appkey}</code>\n"
                            "Add to: <i>Header</i>\n"
                            "\n"
                            "If you are inactive for a long time, the user will be deleted from the database. You will be able to register again after.\n"
                    )
            
            await message.answer(text_get_key, parse_mode="HTML")
















# main def polling
async def main_bot() -> None:
    await dp.start_polling(bot, skip_updates=False) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей


# Start polling
if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except Exception as e:
        #logging.error(f"An error occurred: {e}. Restarting after a delay...")
        print(f"An error occurred: {e}. Restarting after a delay...")
