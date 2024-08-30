import logging

# logging.getLogger('aiogram').propagate = True # Блокировка логирование aiogram до его импорта
# logging.basicConfig(level=logging.INFO, filename='log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл

from keys import (token_telegram)

import time
import sys
import re
import os
import asyncio
from pathlib import Path
from aiogram import Bot, Dispatcher, types, F, Router
# from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import csv
import datetime
from io import StringIO, BytesIO

# from worker_db import ()


dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token_telegram) # Initialize Bot instance with a default parse mode which will be passed to all API calls




# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')
    # await asyncio.sleep(5)



# Push /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    # Menu bot
    # bot_commands = [
    #     BotCommand(command="/menu", description="Главное меню | Main Menu"),
    # ]
    # await bot.set_my_commands(bot_commands)



    ###### Get All data user on telegram ######
    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    is_admin = False
    is_block = False
    is_good = 3
    # admin_id = admin_user_ids[1:-1]
    ###### Get All data user on telegram ######

    #logging.info(f"User {id} press /start")

    # Checking and added the parameters
    # if str(id) in admin_user_ids:
    #     is_admin = True
    #     logging.info(f"The user id:{id} is assigned as an admin.")
    # if str(id) in block:
    #     is_block=True
    #     logging.info(f"The user id:{id} is assigned as an blocked.")
    # if str(name) in oppas:
    #     await bot.send_message(admin_id, f"Пользователь @{name} с id: {id} только что подключился к боту.", parse_mode="HTML")
    #     logging.info(f"The user id:{id} in on system !!!.")

    # Preparing data for the user
    user_data = {"id": id, "name": name, "full_name": full_name, "first_name":first_name,\
                    "last_name": last_name, "chat_id": chat_id, "is_admin": is_admin,\
                    "is_block":is_block, "is_good": is_good}
    
    # If user id has in a Base - update data, else - create user to Base
    # is_on_user = await get_user_by_id(id)
    # if is_on_user is not None:
    #     await update_user(id, user_data)
    # else:
    #     await adding_user(user_data)
    #     await add_settings(id)
    #     await add_discussion(id)
    
    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "bro"))

    # Checking and added the parameters in Settings to white list users And gives them money
    # if str(id) in white_list:
    #     money = 1000 # Yep!
    #     updated_data = {"money": money}
    #     confirmation = await update_settings(id, updated_data) # Gives money
    #     if confirmation is True: # Подтверждение из worcker_db
    #         logging.info(f"1000 RUB added, he id is:{id}.")
    #     else:
    #         logging.error(f"A 1000 RUB has not added, he id is:{id}.")

    await message.answer(f"Hi {about}!\n\n"
                        "You are registered in the AI API, your data is for using the API:\n\n"
                        "*Username:*\n"
                        "username: Vlad\n"
                        "Add to: Json\n"
                        "\n\n"
                        "*API Key:*\n"
                        "Key: appkey\n"
                        "Value: fdft5j5445dfftghd334\n"
                        "Add to: Header")








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
