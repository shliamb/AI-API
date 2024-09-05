# Base
import logging
# logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
logging.basicConfig(level=logging.INFO, filename='./log/app.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
import re
import random
import os
import asyncio
from io import StringIO, BytesIO
import uuid
from pathlib import Path # Работа с файловыми путями 
from datetime import datetime, timezone, timedelta
# import time
# import sys
import csv
# import datetime

# Aiogram
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Service
from worker_db import get_user_by_id, get_user_by_username, update_user, adding_user, get_user_by_username
from backupdb import backup_db
from restore_db import restore_db
from general_functions import day_utcnow, unformat_date
from config import money_to_start, my_app_key, time_correction, min_pay
from keys import token_telegram, is_admin


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





# Статистика минимальная и вычитание суммы
# Очистка базы - два варианта, от клиентов мертвых, от старой статистики
# Кнопка в админке забрать лог, чистка логов
# Восстановление базы
# Ключ от Gemini получил, теперь ее тоже можно прикрутить и попробовать.
# Передача сигнала телеграмм боту, администратору
# Список пользователей









#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    # Menu bot
    bot_commands = [
       BotCommand(command="/menu", description="MENU"),
       BotCommand(command="/my_key", description="Show Key"),
       BotCommand(command="/balance", description="Balance"),
       BotCommand(command="/add_money", description="Add Money"),
       BotCommand(command="/get_stat", description="Get Stats"),
       BotCommand(command="/reset_key", description="Reset Key"),
       BotCommand(command="/help", description="Help"),
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
        await message.answer("You are already registered in the system! Chek your key - /my_key") # Уже есть

    if is_on_user is None:

        while True: # Сразу проверяю на уникальность в базе Username, если не уникально, то генерим по новой, пока не попадем на уникальный вариант
            data_by_username = await get_user_by_username(username)
            if data_by_username is not None:
                username = await gen_username(about) # Генерим заново
            else:
                break
        
        if data_by_username is None: # Зачем то перепроверяю, хз

            last_act_to_base = await day_utcnow(time_correction) # Записываю дату и время

            user_data = {
                "id": id,
                "name": name,
                "full_name": full_name,
                "first_name":first_name,
                "last_name": last_name,
                "username": username,
                "money": money_to_start,
                "date_last_activ": last_act_to_base,
                        }

            await adding_user(user_data)

            is_on_user = await get_user_by_id(id)
            # last_a = is_on_user.date_last_activ
            # current_datetime = await unformat_date(last_a) 
            text_get_key = (  
                "Use the following keys to use the API:\n\n"
                "<b>Username:</b>\n"
                f"Username: <code>{is_on_user.username}</code>\n"
                "Add to: <i>Json</i>\n"
                "\n"
                "<b>API Key:</b>\n"
                f"Key: <code>{my_app_key}</code>\n"
                f"Value: <code>{is_on_user.appkey}</code>\n"
                "Add to: <i>Header</i>\n"
                "\n"
                "If you are inactive for a long time, the user will be deleted from the database. You will be able to register again after.\n"
                "\n"
                f"You have <b>{is_on_user.money}</b> $ to your balance.\n"
                "\n"
                "If you don't understand anything - /help \n"
                # f"Last user activity is - {current_datetime}"
                    )
            
            await message.answer(text_get_key, parse_mode="HTML")


#### Push /MENU ####
@dp.message(Command("menu"))
async def main_menu(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')

    await message.answer(
        "<b>MAIN MENU:</b> \n\n"
        "/my_key - View your API key\n\n"
        "/balance - View your account balance\n\n"
        "/add_money - Add $ to your account*\n\n"
        "/get_stat - Get statistics*\n\n"
        "/reset_key - Change the API key\n\n"
        "/help - Learn more about the API\n\n"
        , parse_mode="HTML")



#### Push /my_key ####
@dp.message(Command("my_key"))
async def my_key(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)
    data = await get_user_by_id(id)

    text_get_key = (  
        "Use the following keys to use the API:\n\n"
        "<b>Username:</b>\n"
        f"Username: <code>{data.username}</code>\n"
        "Add to: <i>Json</i>\n"
        "\n"
        "<b>API Key:</b>\n"
        f"Key: <code>{my_app_key}</code>\n"
        f"Value: <code>{data.appkey}</code>\n"
        "Add to: <i>Header</i>\n"
        "\n"
        "If you are inactive for a long time, the user will be deleted from the database. You will be able to register again after.\n"
        "\n"
        f"You have <b>{data.money}</b> $ to your balance.\n"
        "\n"
        "If you don't understand anything - /help \n"
        # f"Last user activity is - {current_datetime}"
            )
            
    await message.answer(text_get_key, parse_mode="HTML")


#### Push /balance ####
@dp.message(Command("balance"))
async def balance(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)
    data = await get_user_by_id(id)
    await message.answer(f"Your Balance is {data.money} $", parse_mode="HTML")







#### Push /add_money ####

# Set State
class Form_my_pay(StatesGroup):
    add_summ = State()
    confirm_summt = State()

@dp.message(Command("add_money"))
async def add_money(message: types.Message, state: FSMContext):
    # await bot.send_chat_action(message.chat.id, action='typing')
    # id = user_id(message)
    # data = await get_user_by_id(id)
    #await message.answer(f"Your Balance is {data.money} $", parse_mode="HTML")

    await message.answer("Enter the deposit amount in USD:", reply_markup=ReplyKeyboardRemove())

    # await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения в RUB:\nEnter the deposit amount in RUB:", reply_markup=ReplyKeyboardRemove()) # !!!!
    # await bot.answer_callback_query(callback_query.id) # Закрытие сесси кнопки
    await state.set_state(Form_my_pay.add_summ) # Ожидание следующего шага


# Вызов у админа кнопки подтверждения
async def confirm_my_pyz(id, summ, admin_id, mes_id, url):
    # Кнопка подтверждения
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👛 Подтвердить", callback_data=f"confirm_summ_user_d:{id}:{summ}:{admin_id}:{mes_id}")], 
        ]
    )
    await bot.send_message(admin_id, f"User: <a href='{url}'>{id}</a>, he wants to top up his account on: {summ} $", parse_mode="HTML", reply_markup=keyboard)
    await bot.send_message(mes_id, f"The request has been accepted, wait.")
    return


# Ожидание получения суммы пополнения
@dp.message(Form_my_pay.add_summ, F.content_type.in_({'text'}))
async def invoice_user_1(message: Message, state: FSMContext):

    mes_id = message.chat.id
    summ = message.text
    id = user_id(message)
    admin_id = is_admin
    url = f"tg://user?id={id}"

    # Проверка на число
    if message.text.isdigit() is not True:
        await bot.send_message(message.chat.id, f"Enter only the amount in numbers in USD.")
        return

    if float(summ) < min_pay:
        await bot.send_message(message.chat.id, f"The minimum amount is {min_pay} $.")
        return

    # запускаю функцию и передаю данные для подтверждения админом.
    await confirm_my_pyz(id, summ, admin_id, mes_id, url)

    # Закрытие Stats
    await state.clear()


# Обработчик подтверждения
@dp.callback_query(lambda c: c.data and c.data.startswith('confirm_summ_user_d'))
async def confirm_callback_handler_d(callback_query: types.CallbackQuery):
    data = callback_query.data.split(':')
    if len(data) == 5:
        id = int(data[1])
        summ = float(data[2])
        admin_id = int(data[3])
        mes_id = int(data[4])
    else:
        await bot.answer_callback_query(callback_query.id, text="Error in the request data.", show_alert=True)
        return

    data_set = await get_user_by_id(id)
    new_money = data_set.money + float(summ)

    updated_data = {"money": new_money}
    conf = await update_user(id, updated_data)

    if conf is True:
        await bot.send_message(admin_id, f"Customer's account {id} replenished, shared:  {new_money} $.")
        await bot.send_message(mes_id, f"Your account has been topped up with {summ} $.")
        await bot.answer_callback_query(callback_query.id)
        return
    else:
        await bot.send_message(admin_id, f"Replenishment error.")
        await bot.answer_callback_query(callback_query.id)
        return
####







#### Push /get_stat ####
@dp.message(Command("get_stat"))
async def get_stat(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)
    data = await get_user_by_id(id)
    await message.answer(f"Your Balance is {data.money} $", parse_mode="HTML")


#### Push /reset_key ####
@dp.message(Command("reset_key"))
async def reset_key(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)
    new_key = str(uuid.uuid4())

    updated_data = {"appkey": new_key,}

    confirm = await update_user(id, updated_data)
    
    if confirm is True:
        await message.answer(f"Your new Key is: <code>{new_key}</code>", parse_mode="HTML")
    else:
        await message.answer("Sorry, error, try again later.")


#### Push /help ####
@dp.message(Command("help"))
async def help(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    await message.answer(f"There will be instructions for working with the API", parse_mode="HTML")






#### WORK MENU ADMIN ####

# Admin menu
@dp.message(Command("admin"))
async def admin(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)

    # Check access
    if id != is_admin:
        await message.answer(f"Sorry, access is denied.")
        return

    await message.answer(
        "<b>ADMIN MENU:</b> \n\n"
        "/backup - Make a backup of the database\n\n"
        "/admin_stat \n\n"
        "/get_log \n\n"
        "/clear_log \n\n"
        "clear \n"
        "   │ \n"
        "   ├── /clear_old_users - Deleting old users* \n"
        "   └── /clear_db - Cleaning up old DB data* \n\n"
        "/restore_db - Restoring a DB from a file*\n\n"
        , parse_mode="HTML")



# Admin BackupDB
@dp.message(Command("backup"))
async def backup(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)

    # Check access
    if id != is_admin:
        await message.answer(f"Sorry, access is denied.")
        return

    confirmation = backup_db() # - резервная копия
    if confirmation is True:
        await message.answer("The backup copy of the database was created successfully and is presented below. The 3 latest versions are saved in the working folder, the rest are deleted.")
    else:
        await message.answer("Error creating a backup copy of the database.")

    await asyncio.sleep(0.5)

    data_folder = Path("./backup_db/")

    files = [entry for entry in data_folder.iterdir() if entry.is_file()] # Получаем список всех файлов в директории

    sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True) # Сортируем список файлов по дате изменения (от новых к старым)

    for file_to_delete in sorted_files[3:]: # Оставляем последние 3 файла, удаляем остальные
        os.remove(file_to_delete)
    logging.info("Remove all file DB, saved 3 latest files.")

    last_downloaded_file = sorted_files[0] if sorted_files else None   # Последний скачанный файл будет первым в отсортированном списке (новейшим) (адрес)
    logging.info("Download last DB file.")

    await message.bot.send_document(chat_id=message.chat.id, document=types.input_file.FSInputFile(last_downloaded_file))


# Admin submenu stat
@dp.message(Command("admin_stat"))
async def get_admin_stat(message: types.Message):

    data = await get_user_by_username()

    all_static = []
    number = 0
    all_static.append(["№", "Username", "is_failed", "is_block", "date_block", "date_last_activ", "money",\
                        "id", "name", "full_name", "first_name", "last_name"]) # First a names row
    
    for it in data:
        number += 1
        Username = it.Username
        is_failed = it.is_failed
        is_block = it.is_block
        date_block = it.date_block
        date_last_activ = it.date_last_activ
        money = round(it.money, 5)
        id = it.id
        name = it.name
        full_name = it.full_name
        first_name = it.first_name
        last_name = it.last_name

        all_static.append([number, Username, is_failed, is_block, date_block, date_last_activ, money, id, name, full_name,\
                            first_name, last_name]) # added user data

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()


    # csv file to download
    file_name = f"Admin-{datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    except:
        print(f"Error sending documentb Admin stat")


# Admin submenu download log
@dp.message(Command("get_log"))
async def admin_get_log(message: types.Message):

    if os.path.exists("./log/app.log") and os.path.getsize("./log/app.log") > 0:
        await bot.send_document(message.chat.id, document=types.input_file.FSInputFile("./log/app.log"))
    else:
        await bot.send_message(message.chat.id, "The app.log file is empty or missing.")


# Admin clear log /clearlog
@dp.message(Command("clear_log"))
async def admin_clear_log(message: types.Message):

    if os.path.exists("./log/app.log") and os.path.getsize("./log/app.log") > 0:

        with open("./log/app.log", 'w'):
            pass
        await bot.send_message(message.chat.id, "The app.log file has been cleared successfully.")
    else:
        await bot.send_message(message.chat.id, "The app.log file is empty or missing.")


# Admin Clear Old Users
@dp.message(Command("clear_old_users"))
async def clear_old_users(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)

    # Check access
    if id != is_admin:
        await message.answer(f"Sorry, access is denied.")
        return
    # Тут, нужно получить все id пользователей, а затем поочереди по их id забирать их дату последнего посещения и баланс, если он равен или меньше 5$
    # отнимать ее от текущей и при критичном сроке, допустим равным 1 месяцу или больше, запускать удаление строки
    # из таблицы пользователя по id, так же по id удалять все транзакции в таблице статистики
    #
    # Скорее всего можно сделать такой запрос к базе и все с джоинами и всякой херней.
    return


# Admin Clear DB
@dp.message(Command("clear_db"))
async def clear_db(message: types.Message):
    await bot.send_chat_action(message.chat.id, action='typing')
    id = user_id(message)

    # Check access
    if id != is_admin:
        await message.answer(f"Sorry, access is denied.")
        return
    # Нужно удалить все транзакции которые старше месяца допустим, возможно выйдет сделать такую функцию в базе и там все это проделать, без пйтана, посмотрим.
    return


#
# Admin Restore DB
#
# Нажимаю кнопку восстановления, прикрепляю свой файл db бинарный в .sql, он загружается в папку download_db.
# Далее скрипт останавливает все запросы и очищает память, выставляется глобальный флаг, который не допускает  
# пользователям взаимодействовать с базой. Тем временем, очищается полностью и даже разметка работающей базы 
# и полностью переписывается с закаченного файла. Он не удаляется из папки, не думаю что их будет много.
#
 
# class Restor_db(StatesGroup):
#     load_db = State()
#     #restor_db = State()

# # Push button - restore
# @dp.callback_query(lambda c: c.data == 'restore_db')
# async def process_sub_admin_stat(callback_query: types.CallbackQuery, state: FSMContext):
#     await callback_query.message.answer(text="Прикрепи и отправь нужную копию базы данных для восстановления.", reply_markup=ReplyKeyboardRemove())
#     await state.set_state(Restor_db.load_db) # Next Step
#     await bot.answer_callback_query(callback_query.id) # End typing

# # Next step - download db and restore
# @dp.message(Restor_db.load_db)
# #async def student_name(message: Message, state: FSMContext):
# async def load_a_base(message: Message, state: FSMContext):
#     global work_in_progress
#     work_in_progress = True # Блокировка обращений к базе данных всех пользователей


#     if not isinstance(message.document, types.Document):
#         await message.answer("Вы передали не документ.")
#         return

#     file_extension = message.document.file_name.split('.')[-1]
#     allowed_extensions = ['sql']

#     if file_extension not in allowed_extensions:
#         await message.answer("Вы передали файл не sql расширения.")
#         return    


#     # Name file
#     date_time = datetime.datetime.utcnow() # Current date and time
#     formtime = date_time.strftime("%Y-%m-%d-%H-%M")
#     file_name = f"uploaded-db-{formtime}.sql"

#     # await asyncio.sleep(0.3)

#     file_path = f"./download_db/{file_name}"
#     await bot.download(message.document, file_path) # То что прикрепили и отправили, скачивается в папку с новым именем

#     await bot.session.close()
#     await dp.storage.close()

#     confirmation = restore_db(file_path) # Восстановелние базы

#     work_in_progress = False # Восстановление возможности обращения пользователей к базе

#     if confirmation == True:
#         await message.answer("Восстановление базы данных прошло успешно.")
#     else:
#         await message.answer("При восстановлении базы данных, что то пошло не так.")


#     await state.clear()
#     #await state.set_state(Restor_db.restor_db) # Переход к следующему шагу















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