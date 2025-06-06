# Base
import logging
logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
logging.basicConfig(format='%(message)s', level=logging.INFO) # filename='./log/bot.log',
# logging.basicConfig(level=logging.INFO, filename='./log/bot.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
import re
import random
import os
import asyncio
from io import StringIO, BytesIO
import uuid
import json
from pathlib import Path # Работа с файловыми путями 
# from datetime import datetime, timezone, timedelta
# import time
# import sys
import csv
# Aiogram
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import Message, BotCommand, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton #, LabeledPrice, ContentType, InputFile, Document, PhotoSize
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Service
from worker_db import read_user, add_user, update_user, add_account, update_account
# from backupdb import backup_db
# from restore_db import restore_db
from general_functions import day_utcnow
from config import MONEY_TO_START, MY_APP_KEY, COUNTS_QUANTITY, NOTIFICATION
from keys import TOKEN_TELEGRAM, IS_ADMIN


dp = Dispatcher()
bot = Bot(TOKEN_TELEGRAM)


#########
# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')
    # await asyncio.sleep(5)


# Forced Start:
async def forced_start(message: types.Message):
    language_code = message.from_user.language_code
    if language_code == "ru":
        await message.answer("Обновлен бот. Для продолжения нажмите /start.  ", parse_mode="HTML")
    else:
        await message.answer("Updated the bot. To continue, press /start", parse_mode="HTML")


########



# START:
class Form_start(StatesGroup):
    captcha = State()

@dp.message(Form_start.captcha)
async def registration_telegram_user(message: Message, state: FSMContext) -> None:

    send_data = await state.get_data()
    cldata = send_data.get("send_data")
    answerq = str(cldata.get("answerq"))
    user_data = cldata.get("user_data")
    id = user_data.get("id")
    language = user_data.get("language")

    if message.text != answerq:
        logging.error(f"Error bot: user registration wrong captcha id: {id}")
        if language == "en":
            await message.answer("Wrong answer, try again - /start")
        elif language == "ru":
            await message.answer("Не верный ответ, попробуй еще раз - /start")
        await state.clear()
        return

    confirm = await add_user(user_data)
    if not confirm:
        logging.error(f"Error bot: Don't save new user: {id}")
        return

    if language == "en":
        await message.answer("Successful registration.\nNow you can add API accesses - /my_key.")
    elif language == "ru":
        await message.answer("Успешная регистрация.\nТеперь вы можете добавлять доступы к API - /my_key.")

    await state.clear()




#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await typing(message)

    # Menu bot
    bot_commands = [
       BotCommand(command="/menu", description="MENU"),
       BotCommand(command="/accounts", description="ACCOUNTS"),
       #BotCommand(command="/balance", description="Balance"),
       #BotCommand(command="/add_money", description="Add Money"),
       #BotCommand(command="/get_stat", description="Get Stats"),
       #BotCommand(command="/reset_key", description="Reset Key"),
       #BotCommand(command="/prices", description="Prices"),
       BotCommand(command="/help", description="GUIDE"),
    ]
    await bot.set_my_commands(bot_commands)


    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code # ??

    is_on_user = await read_user(id) # Получаем по ID данные из базы

    if is_on_user:
        lan = is_on_user.get("language")
        if lan == "en":
            await message.answer("You are already registered.")
            return
        elif lan == "ru":
            await message.answer("Вы уже зарегистрированны.")
            return

    # Тупейшая проверка на бота
    a, b = random.randint(1, 10), random.randint(1, 10)
    op = random.choice(['+', '-'])
    answerq = eval(f"{a}{op}{b}")
    question = f'{a} {op} {b} = ?'

    user_data = {
        "user_id": id,
        "name": name,
        "full_name": full_name,
        "first_name":first_name,
        "last_name": last_name,

        "money": MONEY_TO_START,
        "last_visit": await day_utcnow(),
        "language": language_code,
        "counts_api": COUNTS_QUANTITY,
        "notifications": NOTIFICATION
    }

    send_data = {'answerq':answerq, 'user_data': user_data}

    await state.update_data(send_data=send_data)

    if language_code == "en":
        await message.answer(f"{question}")
    elif language_code == "ru":
        await message.answer(f"{question}")

    await state.set_state(Form_start.captcha)





#### Push /MENU ####
@dp.message(Command("menu"))
async def main_menu(message: types.Message):
    await typing(message)

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    language = data.get("language")
    money = round(data.get("money"), 2)
    list_access_id = data.get("list_access_id")
    list_access_id = json.loads(list_access_id) if list_access_id else []
    accounts = len(list_access_id)
    raw_notifications = data.get("notifications")
    notifications_ru = "ВКЛ." if raw_notifications else "ВЫКЛ."
    notifications_en = "ON" if raw_notifications else "OFF"

    ru_text = f'''

<b>🎛 ГЛАВНОЕ МЕНЮ:</b>

<b>🔑 АККАУНТЫ: {accounts} шт.</b>
        Управление – /accounts

<b>💳 БАЛАНС: {money}$</b>
        Пополнить – /pay

<b>📊 СТАТИСТИКА:</b>
        Получить exel – /stat

<b>🔌 НАСТРОЙКИ:</b>
        Язык: <b>{(language).upper()}</b> – /lang
        Увед-ия: <b>{notifications_ru}</b> – /note

    '''

    en_text = f'''

<b>🎛 MAIN MENU:</b>

<b>🔑 ACCOUNTS: {accounts} pieces</b>
        Management – /accounts

<b>💳 MONEY BALANCE: {money}$</b>
        Deposit – /pay

<b>📊 STATISTICS:</b>
        Get an exel – /stat

<b>🔌 SETTINGS:</b>
        Language: <b>{(language).upper()}</b> – /lang
        Notifications: <b>{notifications_en}</b> – /note

    '''

    if language == "en":
        await message.answer(en_text, parse_mode="HTML")
    else:
        await message.answer(ru_text, parse_mode="HTML")



#### Push /LANG ####
@dp.message(Command("lang"))
async def change_language(message: types.Message):
    await typing(message)

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    language = data.get("language")
    language = "en" if language == "ru" else "ru"
    new_data = {"user_id": id, "language": language}

    confirm = await update_user(new_data)
    if not confirm:
        return

    await main_menu(message)

    if language == "ru":
        await message.answer("Язык интерфейса изменен", parse_mode="HTML")
    else:
        await message.answer("The interface language has been changed", parse_mode="HTML")



#### Push /note ####
@dp.message(Command("note"))
async def change_notifications(message: types.Message):
    await typing(message)

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    language = data.get("language")
    notifications = False if data.get("notifications") else True
    new_data = {"user_id": id, "notifications": notifications}

    confirm = await update_user(new_data)
    if not confirm:
        return

    await main_menu(message)

    if language == "ru":
        await message.answer("Уведомления отключены", parse_mode="HTML")
    else:
        await message.answer("Notifications are disabled", parse_mode="HTML")






#### Push /accounts ####
@dp.message(Command("accounts"))
async def accounts_menu(message: types.Message):
    await typing(message)

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    language = data.get("language")
    list_access_id = data.get("list_access_id")
    list_access_id = json.loads(list_access_id) if list_access_id else []
    accounts = len(list_access_id)
    counts_api = data.get("counts_api")

    ru_text = f'''

<b>🔑 АККАУНТЫ: {accounts} шт.</b>

<b>🔌 1 Аккаунт</b>
        ключ

        

🔗 Добавить ({counts_api}) - /add_acc


👈 Назад – /back

    '''

    en_text = f'''

<b>🎛 MAIN MENU:</b>

<b>🔑 ACCOUNTS: {accounts} pieces</b>

    '''

    if language == "en":
        await message.answer(en_text, parse_mode="HTML")
    else:
        await message.answer(ru_text, parse_mode="HTML")



#### Push /back ####
@dp.message(Command("back"))
async def back_main_menu(message: types.Message):
    await main_menu(message)



#### Push /add_acc ####
@dp.message(Command("add_acc"))
async def add_accounts(message: types.Message):
    await typing(message)

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    language = data.get("language")
    list_access_id = [] if not data.get("list_access_id") else json.loads(data.get("list_access_id"))
    counts_api = data.get("counts_api")


    if counts_api == 0:
        if language == "ru":
            await message.answer("Вы исчерпали лимит общего колличества аккаунтов соединения с API. Удалите часть созданных.", parse_mode="HTML")
        else:
            await message.answer("You have reached the limit of the total number of accounts connected to the API. Delete some of the created ones.", parse_mode="HTML")
        return

    new_access_id = uuid.uuid4()
    list_access_id.append(str(new_access_id))
    counts_api = counts_api - 1

    update_data_account = {"access_id": new_access_id, "api_key": MY_APP_KEY, "api_value": uuid.uuid4(), "user_id_telegram": id}

    if not await add_account(update_data_account):
        logging.error(f"Error add_account user - {id}")
        return

    update_data_user = {"user_id": id, "counts_api": counts_api, "list_access_id": json.dumps(list_access_id)}
    if not await update_user(update_data_user):
        logging.error(f"Error update_user user - {id}")
        return

    await accounts_menu(message)

    if language == "ru":
        await message.answer("Доступ к API создан успешно", parse_mode="HTML")
    else:
        await message.answer("API access was created successfully", parse_mode="HTML")



























# #### Push /my_key ####
# @dp.message(Command("my_key"))
# async def my_key(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)
#     data = await get_user_by_id(id)

#     text_get_key = f''' 
# Use the following keys to use the API:

# <b>USERNAME:</b>
#     Username: <code>{data.username}</code>
#     Add to: <i>Form-data</i>

# <b>API KEY:</b>
#     Key: <code>{MY_APP_KEY}</code>
#     Value: <code>{data.appkey}</code>
#     Add to: <i>Header</i>

# "If you are inactive for a long time, the user will be deleted from the database. You will be able to register again after.

# You have <b>{data.money}</b> $ to your balance.

# If you don't understand anything - /help 
#     '''
            
#     await message.answer(text_get_key, parse_mode="HTML")





# #### Push /balance ####
# @dp.message(Command("balance"))
# async def balance(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)
#     data = await get_user_by_id(id)
#     await message.answer(f"Your Balance is {data.money} $", parse_mode="HTML")







# #### Push /add_money ####

# # Set State
# class Form_my_pay(StatesGroup):
#     add_summ = State()
#     confirm_summt = State()

# @dp.message(Command("add_money"))
# async def add_money(message: types.Message, state: FSMContext):
#     # await bot.send_chat_action(message.chat.id, action='typing')
#     # id = user_id(message)
#     # data = await get_user_by_id(id)
#     # await message.answer(f"Your Balance is {data.money} $", parse_mode="HTML")

#     await message.answer("Enter the deposit amount in USD:", reply_markup=ReplyKeyboardRemove())

#     # await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения в RUB:\nEnter the deposit amount in RUB:", reply_markup=ReplyKeyboardRemove()) # !!!!
#     # await bot.answer_callback_query(callback_query.id) # Закрытие сесси кнопки
#     await state.set_state(Form_my_pay.add_summ) # Ожидание следующего шага


# # Вызов у админа кнопки подтверждения
# async def confirm_my_pyz(id, summ, admin_id, mes_id, url):
#     # Кнопка подтверждения
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text="👛 Подтвердить", callback_data=f"confirm_summ_user_d:{id}:{summ}:{admin_id}:{mes_id}")], 
#         ]
#     )
#     await bot.send_message(admin_id, f"User: <a href='{url}'>{id}</a>, he wants to top up his account on: {summ} $", parse_mode="HTML", reply_markup=keyboard)
#     await bot.send_message(mes_id, f"The request has been accepted, wait.")
#     return


# # Ожидание получения суммы пополнения
# @dp.message(Form_my_pay.add_summ, F.content_type.in_({'text'}))
# async def invoice_user_1(message: Message, state: FSMContext):

#     mes_id = message.chat.id
#     summ = message.text
#     id = user_id(message)
#     admin_id = IS_ADMIN
#     url = f"tg://user?id={id}"

#     # Проверка на число
#     if message.text.isdigit() is not True:
#         await bot.send_message(message.chat.id, f"Enter only the amount in numbers in USD.")
#         return

#     if float(summ) < MIN_PAY:
#         await bot.send_message(message.chat.id, f"The minimum amount is {MIN_PAY} $.")
#         return

#     # запускаю функцию и передаю данные для подтверждения админом.
#     await confirm_my_pyz(id, summ, admin_id, mes_id, url)

#     # Закрытие Stats
#     await state.clear()


# # Обработчик подтверждения
# @dp.callback_query(lambda c: c.data and c.data.startswith('confirm_summ_user_d'))
# async def confirm_callback_handler_d(callback_query: types.CallbackQuery):
#     data = callback_query.data.split(':')
#     if len(data) == 5:
#         id = int(data[1])
#         summ = float(data[2])
#         admin_id = int(data[3])
#         mes_id = int(data[4])
#     else:
#         await bot.answer_callback_query(callback_query.id, text="Error in the request data.", show_alert=True)
#         return

#     data_set = await get_user_by_id(id)
#     new_money = data_set.money + float(summ)

#     updated_data = {"money": new_money}
#     conf = await update_user(id, updated_data)

#     if conf is True:
#         await bot.send_message(admin_id, f"Customer's account {id} replenished, shared:  {new_money} $.")
#         await bot.send_message(mes_id, f"Your account has been topped up with {summ} $.")
#         await bot.answer_callback_query(callback_query.id)
#         return
#     else:
#         await bot.send_message(admin_id, f"Replenishment error.")
#         await bot.answer_callback_query(callback_query.id)
#         return
# ####







# #### Push /get_stat ####
# @dp.message(Command("get_stat"))
# async def get_stat_user(message: types.Message):

#     id = user_id(message)
#     data_user_id = await get_user_by_id(id)


#     data = await get_last_statistics(data_user_id.username)

#     all_static = []
#     number = 0
#     all_static.append(["№", "№", "username table stat", "time", "use model", "sesion token/img/min", "price 1 tok/img/min", "total_price", "id telegram"]) # First a names row
    
#     for it in data:
#         number += 1
#         id_table = it.id
#         username_table_stat = it.username_table_stat
#         time = it.time
#         use_model = it.use_model
#         sesion_token = it.sesion_token
#         price_1_tok = it.price_1_tok
#         total_price = it.total_price


#         all_static.append([number, id_table, username_table_stat, time, use_model, sesion_token, price_1_tok, total_price, id]) # added user data

#     # Create csv file
#     output = StringIO()
#     writer = csv.writer(output)
#     for row in all_static:
#         writer.writerow(row)
#     csv_data = output.getvalue()
#     output.close()


#     # csv file to download
#     file_name = f"User-statistic-{str(random.randint(30, 40))}.csv"
#     buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
#     try:
#         await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
#     except:
#         print(f"Error sending documentb User stat")





# #### Push /reset_key ####
# @dp.message(Command("reset_key"))
# async def reset_key(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)
#     new_key = str(uuid.uuid4())

#     updated_data = {"appkey": new_key,}

#     confirm = await update_user(id, updated_data)
    
#     if confirm is True:
#         await message.answer(f"Your new Key is: <code>{new_key}</code>", parse_mode="HTML")
#     else:
#         await message.answer("Sorry, error, try again later.")



# # MENU: PRICES:
# @dp.message(Command('prices'))
# async def get_prices(message: types.Message):

#     id = user_id(message)


#     prices_en = '''

#     OpenAI language model 1 million tokens in $:
#         'gpt-4.1': 12,
#         'gpt-4.1-mini': 2.4,
#         'o1-pro': 900,
#         'gpt-4.1-nano': 0.6,
#         'gpt-4.5-preview': 270,
#         'o1': 90,
#         'o3': 60,
#         'o1-preview': 90,
#         'o1-mini': 6.6,
#         'o3-mini': 6.6,
#         'o4-mini': 6.6,
#         'chatgpt-4o-latest': 24,
#         'gpt-4o': 24,
#         'gpt-4o-2024-05-13': 24,
#         'gpt-4o-2024-08-06': 15,
#         'gpt-4o-mini': 1.8, # no vision
#         'gpt-4o-mini-2024-07-18': 1.8, # no vision
#         'gpt-4-turbo-2024-04-09': 48,

#     The language model from Google is 1 million in $:
#         'gemini-2.5-pro-preview-05-06': 13.5,
#         'gemini-2.5-flash-preview-04-17': 0.9,
#         'gemini-2.0-flash-exp': 0.9,
#         'gemini-2.0-flash-lite-001': 0.45,
#         'gemini-1.5-pro-latest': 3.75,
#         'gemini-1.5-flash-latest': 0.225,
#         'gemini-1.5-flash-8b': 0.5,
    
#     The language model from Elon Musk Grok is 1 million in $:
#         'grok-3-latest': 21.6,
#         'grok-3-fast-latest': 36, 
#         'grok-3-mini-latest': 0.96,
#         'grok-3-mini-fast-latest': 5.52,
#         'grok-vision-beta': 24,
#         'grok-2-vision-latest': 14.4,
#         'grok-2-latest': 14.4,
#         'grok-beta': 24,

#     The language model from Anthropic is 1 million in $:
#         'claude-3-7-sonnet-latest': 21.6,
#         'claude-3-5-sonnet-latest': 21.6,
#         'claude-3-5-haiku-latest': 5.76,
#         'claude-3-opus-latest': 108,
#         'claude-3-sonnet-20240229': 21.6,
#         'claude-3-haiku-20240307': 1.8,

#     Generating images for one in $:
#         'dall-e-3-1024': 0.048,
#         'dall-e-3-1792': 0.096,
#         'dall-e-3-hd-1024': 0.096,
#         'dall-e-3-hd-1792': 0.144,
#         'dall-e-2-1024': 0.024,
#         'dall-e-2-512': 0.0216,
#         'dall-e-2-256': 0.0192,

#     Voice generation of 1M characters in $:
#         'tts-1': 18,
#         'tts-1-hd': 36,

#     Transcription from audio to text min. in $:
#         'whisper-1': 0.0072,

#     '''


#     await message.answer(prices_en, parse_mode="HTML")




# #### Push /help ####
# @dp.message(Command("help"))
# async def help(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     await message.answer(f"Description and instructions are here - https://github.com/shliamb/AI-API-instruction", parse_mode="HTML")






# #### WORK MENU ADMIN ####

# # Admin menu
# @dp.message(Command("admin"))
# async def admin(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)

#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return

#     text = '''

# <b>ADMIN MENU:</b>
#     /backup - make a backup of the database
#     /admin_stat
#     /get_logs

# <b>CLEAR DATA:</b>
#     /clear_logs - deleting logs
#     /clear_old_users - deleting old users*
#     /clear_db - cleaning up old DB data*
#     /restore_db - restoring a DB from a file*

#     '''
#     await message.answer(text, parse_mode="HTML")



# # Admin BackupDB
# @dp.message(Command("backup"))
# async def backup(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)

#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return

#     confirmation = backup_db() # - резервная копия
#     if confirmation is True:
#         await message.answer("The backup copy of the database was created successfully and is presented below. The 3 latest versions are saved in the working folder, the rest are deleted.")
#     else:
#         await message.answer("Error creating a backup copy of the database.")

#     await asyncio.sleep(0.5)

#     data_folder = Path("./backup_db/")

#     files = [entry for entry in data_folder.iterdir() if entry.is_file()] # Получаем список всех файлов в директории

#     sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True) # Сортируем список файлов по дате изменения (от новых к старым)

#     for file_to_delete in sorted_files[3:]: # Оставляем последние 3 файла, удаляем остальные
#         os.remove(file_to_delete)
#     logging.info("Remove all file DB, saved 3 latest files.")

#     last_downloaded_file = sorted_files[0] if sorted_files else None   # Последний скачанный файл будет первым в отсортированном списке (новейшим) (адрес)
#     logging.info("Download last DB file.")

#     await message.bot.send_document(chat_id=message.chat.id, document=types.input_file.FSInputFile(last_downloaded_file))


# # Admin get statistic
# @dp.message(Command("admin_stat"))
# async def get_admin_stat(message: types.Message):
#     id = user_id(message)
#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return

#     data = await get_all_data_user_by_username()

#     all_static = []
#     number = 0
#     all_static.append(["№", "Username", "is failed", "is block", "date block", "date last activ", "money",\
#                         "id", "name", "full name", "first name", "last name"]) # First a names row
    
#     for it in data:
#         number += 1
#         username = it.username
#         is_failed = it.is_failed
#         is_block = it.is_block
#         date_block = it.date_block
#         date_last_activ = it.date_last_activ
#         money = round(it.money, 5)
#         id = it.id
#         name = it.name
#         full_name = it.full_name
#         first_name = it.first_name
#         last_name = it.last_name

#         all_static.append([number, username, is_failed, is_block, date_block, date_last_activ, money, id, name, full_name,\
#                             first_name, last_name]) # added user data

#     # Create csv file
#     output = StringIO()
#     writer = csv.writer(output)
#     for row in all_static:
#         writer.writerow(row)
#     csv_data = output.getvalue()
#     output.close()


#     # csv file to download
#     file_name = f"Admin-statistic-{str(random.randint(30, 40))}.csv"
#     buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
#     try:
#         await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
#     except:
#         print(f"Error sending document Admin stat")


# # Admin submenu download log
# @dp.message(Command("get_logs"))
# async def admin_get_log(message: types.Message):
#     id = user_id(message)
#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return

#     if os.path.exists("./log/bot.log") and os.path.getsize("./log/bot.log") > 0:
#         await bot.send_document(message.chat.id, document=types.input_file.FSInputFile("./log/bot.log"))
#     else:
#         await bot.send_message(message.chat.id, "The bot.log file is empty or missing.")

#     if os.path.exists("./log/api.log") and os.path.getsize("./log/api.log") > 0:
#         await bot.send_document(message.chat.id, document=types.input_file.FSInputFile("./log/api.log"))
#     else:
#         await bot.send_message(message.chat.id, "The api.log file is empty or missing.")


# # Admin clear logs /clearlog
# @dp.message(Command("clear_logs"))
# async def admin_clear_log(message: types.Message):
#     id = user_id(message)
#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return

#     if os.path.exists("./log/bot.log") and os.path.getsize("./log/bot.log") > 0:

#         with open("./log/bot.log", 'w'):
#             pass
#         await bot.send_message(message.chat.id, "The bot.log file has been cleared successfully.")
#     else:
#         await bot.send_message(message.chat.id, "The bot.log file is empty or missing.")

#     if os.path.exists("./log/api.log") and os.path.getsize("./log/api.log") > 0:

#         with open("./log/api.log", 'w'):
#             pass
#         await bot.send_message(message.chat.id, "The api.log file has been cleared successfully.")
#     else:
#         await bot.send_message(message.chat.id, "The api.log file is empty or missing.")


# # Admin Clear Old Users
# @dp.message(Command("clear_old_users"))
# async def clear_old_users(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)

#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return
#     # Тут, нужно получить все id пользователей, а затем поочереди по их id забирать их дату последнего посещения и баланс, если он равен или меньше 5$
#     # отнимать ее от текущей и при критичном сроке, допустим равным 1 месяцу или больше, запускать удаление строки
#     # из таблицы пользователя по id, так же по id удалять все транзакции в таблице статистики
#     #
#     # Скорее всего можно сделать такой запрос к базе и все с джоинами и всякой херней.
#     return


# # Admin Clear DB
# @dp.message(Command("clear_db"))
# async def clear_db(message: types.Message):
#     await bot.send_chat_action(message.chat.id, action='typing')
#     id = user_id(message)

#     # Check access
#     if id != IS_ADMIN:
#         await message.answer(f"Sorry, access is denied.")
#         return
#     # Нужно удалить все транзакции которые старше месяца допустим, возможно выйдет сделать такую функцию в базе и там все это проделать, без пйтана, посмотрим.
#     return


# #
# # Admin Restore DB
# #
# # Нажимаю кнопку восстановления, прикрепляю свой файл db бинарный в .sql, он загружается в папку download_db.
# # Далее скрипт останавливает все запросы и очищает память, выставляется глобальный флаг, который не допускает  
# # пользователям взаимодействовать с базой. Тем временем, очищается полностью и даже разметка работающей базы 
# # и полностью переписывается с закаченного файла. Он не удаляется из папки, не думаю что их будет много.
# #
 
# # class Restor_db(StatesGroup):
# #     load_db = State()
# #     #restor_db = State()

# # # Push button - restore
# # @dp.callback_query(lambda c: c.data == 'restore_db')
# # async def process_sub_admin_stat(callback_query: types.CallbackQuery, state: FSMContext):
# #     await callback_query.message.answer(text="Прикрепи и отправь нужную копию базы данных для восстановления.", reply_markup=ReplyKeyboardRemove())
# #     await state.set_state(Restor_db.load_db) # Next Step
# #     await bot.answer_callback_query(callback_query.id) # End typing

# # # Next step - download db and restore
# # @dp.message(Restor_db.load_db)
# # #async def student_name(message: Message, state: FSMContext):
# # async def load_a_base(message: Message, state: FSMContext):
# #     global work_in_progress
# #     work_in_progress = True # Блокировка обращений к базе данных всех пользователей


# #     if not isinstance(message.document, types.Document):
# #         await message.answer("Вы передали не документ.")
# #         return

# #     file_extension = message.document.file_name.split('.')[-1]
# #     allowed_extensions = ['sql']

# #     if file_extension not in allowed_extensions:
# #         await message.answer("Вы передали файл не sql расширения.")
# #         return    


# #     # Name file
# #     date_time = datetime.datetime.utcnow() # Current date and time
# #     formtime = date_time.strftime("%Y-%m-%d-%H-%M")
# #     file_name = f"uploaded-db-{formtime}.sql"

# #     # await asyncio.sleep(0.3)

# #     file_path = f"./download_db/{file_name}"
# #     await bot.download(message.document, file_path) # То что прикрепили и отправили, скачивается в папку с новым именем

# #     await bot.session.close()
# #     await dp.storage.close()

# #     confirmation = restore_db(file_path) # Восстановелние базы

# #     work_in_progress = False # Восстановление возможности обращения пользователей к базе

# #     if confirmation == True:
# #         await message.answer("Восстановление базы данных прошло успешно.")
# #     else:
# #         await message.answer("При восстановлении базы данных, что то пошло не так.")


# #     await state.clear()
# #     #await state.set_state(Restor_db.restor_db) # Переход к следующему шагу















# main def polling
async def main_bot() -> None:
    await dp.start_polling(bot, skip_updates=False) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей


# Start polling
if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except Exception as e:
        logging.error(f"An error occurred: {e}.")
        print(f"An error occurred: {e}.")














    # chat_id = callback_query.message.chat.id
    # message_id = callback_query.message.message_id