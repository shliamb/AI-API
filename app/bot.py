# Base
from config import MONEY_TO_START, GUEST_APP_KEY, COUNTS_QUANTITY, NOTIFICATION, MIN_PAY, DOWNLOAD, PATH_LOGS
from keys import TOKEN_TELEGRAM, IS_ADMIN
#import logging
#logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
from setup_config_logger import setup_logger
logger_bot = setup_logger('bot', f'{PATH_LOGS}bot.log')
# import re
import random
import os
import asyncio
from io import StringIO #, BytesIO
import uuid
import json
from pathlib import Path # Работа с файловыми путями 
from datetime import datetime
# import time
# import sys
import csv
# Aiogram
from aiogram import Bot, Dispatcher, types, F #, Router
# from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command #, Filter
from aiogram.types import Message, BotCommand, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton #, LabeledPrice, ContentType, InputFile, Document, PhotoSize
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Service
from general_functions import day_utcnow
from worker_db import read_user, add_user, update_user, add_account, read_accounts_user_id, del_account, read_stat_for_user_id, read_users, delete_stat_table, drop_all_tables_and_reset_schema
from backupdb import backup_db
from restore_db import restore_db
from create_tables import create_tables_in_db
from restore_users_to_db import restore_users_to_db
from get_json_old_users import get_json_old_users


dp = Dispatcher()
bot = Bot(TOKEN_TELEGRAM)

PARANOIA_MODE = False




#########
# Get User_ID
def user_id(action) -> int:
    '''Получает user id'''
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    '''На экране будет писать typing...'''
    await bot.send_chat_action(action.chat.id, action='typing')

# Forced Start:
async def forced_start(message: types.Message):
    '''Если в базе нет user, то попросит нажать /start'''
    language_code = message.from_user.language_code
    if language_code == "ru":
        await message.answer("Обновлен бот. Для продолжения нажмите /start.  ", parse_mode="HTML")
    else:
        await message.answer("Updated the bot. To continue, press /start", parse_mode="HTML")

# Mode Paranoia:
async def paranoia_mode(message: types.Message) -> bool:
    '''Блокирует всех кроме админа, если включить в админке режим паранои'''
    if PARANOIA_MODE and user_id(message) != IS_ADMIN:
        language = message.from_user.language_code
        await message.answer("🚧 The bot is in service" if language == "en" else "🚧 Бот на обслуживании", parse_mode="HTML")
        return True


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
        logger_bot.error(f"Error bot: user registration wrong captcha id: {id}")
        if language == "en":
            await message.answer("Wrong answer, try again - /start")
        elif language == "ru":
            await message.answer("Не верный ответ, попробуй еще раз - /start")
        await state.clear()
        return

    confirm = await add_user(user_data)
    if not confirm:
        logger_bot.error(f"Error bot: Don't save new user: {id}")
        return

    if language == "en":
        await message.answer("Successful registration.\nNow you can add API accesses - /accounts")
    elif language == "ru":
        await message.answer("Успешная регистрация.\nТеперь вы можете добавлять доступы к API - /accounts")

    await state.clear()




#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await typing(message)

    if await paranoia_mode(message):
        return

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

    if await paranoia_mode(message):
        return

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    #logger_bot.info(f"Tap menu user_id: {id}")

    language = data.get("language")
    money = round(data.get("money"), 2)
    list_access_id = data.get("list_access_id")
    list_access_id = json.loads(list_access_id) if list_access_id else []
    accounts = len(list_access_id)
    raw_notifications = data.get("notifications")
    notifications_ru = "ВКЛ." if raw_notifications else "ВЫКЛ."
    notifications_en = "ON" if raw_notifications else "OFF"

    # Русская версия
    ru_text = (
        f"<b>🎛 ГЛАВНОЕ МЕНЮ:</b>\n\n"
        f"<b>🔑 АККАУНТЫ: {accounts} шт.</b>\n"
        f"        Управление – /accounts\n\n"
        f"<b>💳 БАЛАНС: {money}$</b>\n"
        f"        Пополнить – /pay\n\n"
        f"<b>💵 Цены:</b>\n"
        f"        Цены на ИИ  – /price\n\n"
        f"<b>📊 СТАТИСТИКА:</b>\n"
        f"        Получить exel – /stat\n\n"
        f"<b>🔌 НАСТРОЙКИ:</b>\n"
        f"        Язык: <b>{language.upper()}</b> – /lang\n"
        f"        Уведомления: <b>{notifications_ru}</b> – /note"
    )

    # Английская версия
    en_text = (
        f"<b>🎛 MAIN MENU:</b>\n\n"
        f"<b>🔑 ACCOUNTS: {accounts} pieces</b>\n"
        f"        Management – /accounts\n\n"
        f"<b>💳 MONEY BALANCE: {money}$</b>\n"
        f"        Deposit – /pay\n\n"
        f"<b>💵 Prices:</b>\n"
        f"        AI prices  – /price\n\n"
        f"<b>📊 STATISTICS:</b>\n"
        f"        Get an exel – /stat\n\n"
        f"<b>🔌 SETTINGS:</b>\n"
        f"        Language: <b>{language.upper()}</b> – /lang\n"
        f"        Notifications: <b>{notifications_en}</b> – /note"
    )

    # Отправка сообщения
    await message.answer(en_text if language == "en" else ru_text, parse_mode="HTML")



#### Push /LANG ####
@dp.message(Command("lang"))
async def change_language(message: types.Message):
    await typing(message)

    if await paranoia_mode(message):
        return

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

    if await paranoia_mode(message):
        return

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

    if await paranoia_mode(message):
        return

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

    #
    coints_text_ru = (
        f"\n🔗 Добавить ({counts_api}) - /addAcc" if counts_api 
        else "\n🔗 Больше добавить нельзя"
    )
    coints_text_en = (
        f"\n🔗 Add ({counts_api}) - /addAcc" if counts_api
        else "\n🔗 You can't add more"
    )

    #
    all_accounts_user = await read_accounts_user_id(id)
    text_accounts = []
    for i, record in enumerate(all_accounts_user, start=1):
        access_id = record.get("access_id")
        api_key = record.get("api_key")
        api_value = record.get("api_value")
        
        account_info = (
            f"\n\n<b>🔌 {i}. {'Аккаунт' if language == 'ru' else 'Account'}:</b>\n"
            f"    <b>- access_id:</b> <code>{access_id}</code>\n"
            f"    <b>- api_key:</b> <code>{api_key}</code>\n"
            f"    <b>- api_value:</b> <code>{api_value}</code>"
        )
        text_accounts.append(account_info)
    text_accounts = "".join(text_accounts)

    #
    text_del_acc_en = "\n💣 Delete accounts - /delAcc" if accounts else ""
    text_del_acc_ru = "\n💣 Удалить аккаунты - /delAcc" if accounts else ""

    #
    ru_text = (
        f"<b>🔑 АККАУНТЫ: {accounts} шт.</b>\n"
        f"{text_accounts}\n"
        f"{coints_text_ru}"
        f"{text_del_acc_ru}\n\n"
        "👈 Назад – /back"
    )

    #
    en_text = (
        f"<b>🔑 ACCOUNTS: {accounts} pieces</b>\n"
        f"{text_accounts}\n"
        f"{coints_text_en}"
        f"{text_del_acc_en}\n\n"
        "👈 Back – /back"
    )

    # Отправляем сообщение
    await message.answer(en_text if language == "en" else ru_text, parse_mode="HTML")



#### Push /back ####
@dp.message(Command("back"))
async def back_main_menu(message: types.Message):
    await main_menu(message)



#### Push /add_acc ####
@dp.message(Command("addAcc"))
async def add_accounts(message: types.Message):

    '''
    list_access_id - хранит список ID для доступа к API в профиле Telegram-пользователя.

    Особенности работы:
    - В базе данных сохраняется как строка (JSON-формат)
    - При чтении из базы автоматически преобразуется в список
    - При сохранении обратно в базу конвертируется в строку

    Пример формата данных:
    - В Python: ['id1', 'id2', 'id3'] 
    - В базе: "['id1', 'id2', 'id3']" (как JSON-строка)
    '''

    await typing(message)

    if await paranoia_mode(message):
        return

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

    update_data_account = {"access_id": new_access_id, "api_key": GUEST_APP_KEY, "api_value": uuid.uuid4(), "user_id_telegram": id}
    if not await add_account(update_data_account):
        logger_bot.error(f"Error add_account user - {id}")
        return

    update_data_user = {"user_id": id, "counts_api": counts_api, "list_access_id": json.dumps(list_access_id)}
    if not await update_user(update_data_user):
        logger_bot.error(f"Error update_user user - {id}")
        return

    await accounts_menu(message)

    if language == "ru":
        await message.answer("Доступ к API создан успешно", parse_mode="HTML")
    else:
        await message.answer("API access was created successfully", parse_mode="HTML")



#### Push /delete accounts users ####
@dp.message(Command("delAcc"))
async def delete_accouts_user(message: types.Message):
    await typing(message)

    if await paranoia_mode(message):
        return

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return
    
    language = data.get("language")
    list_access_id = data.get("list_access_id")
    list_access_id = json.loads(list_access_id) if list_access_id else None

    if list_access_id:
        for access_id in list_access_id:
            if not await del_account(access_id):
                logger_bot.error(f"Error del_accounts user - {id}, access_id - {access_id}")
                await message.answer("Ошибка удаления Аккаунтов" if language == "ru" else "Account Deletion Error", parse_mode="HTML")
                return

    new_data = {"user_id": id, "counts_api": COUNTS_QUANTITY, "list_access_id": None}
    if not await update_user(new_data):
        logger_bot.error(f"Error delete_accouts_user - update_user  - {id}")
        await message.answer("Ошибка сброса counts_api" if language == "ru" else "Counts_api reset error", parse_mode="HTML")
        return

    await accounts_menu(message)
    await message.answer("Аккаунты удалены успешно" if language == "ru" else "Accounts deleted successfully", parse_mode="HTML")






#### Push /add_money ####

# Set State
class Form_my_pay(StatesGroup):
    add_summ = State()
    confirm_summt = State()

@dp.message(Command("pay"))
async def add_money(message: types.Message, state: FSMContext):
    await typing(message)

    if await paranoia_mode(message):
        return

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return
    
    language = data.get("language")
    await message.answer("Введите сумму в долларах" if language == "ru" else "Enter the deposit amount in USD:", reply_markup=ReplyKeyboardRemove())
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
    admin_id = IS_ADMIN
    url = f"tg://user?id={id}"

    # Проверка на число
    if message.text.isdigit() is not True:
        logger_bot.error(f"The minimum amount is {MIN_PAY} $.")
        await bot.send_message(message.chat.id, f"Enter only the amount in numbers in USD.")
        return

    if float(summ) < MIN_PAY:
        logger_bot.error(f"The minimum amount is {MIN_PAY} $.")
        await bot.send_message(message.chat.id, f"The minimum amount is {MIN_PAY} $.")
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

    data_set = await read_user(id)
    new_money = data_set.get("money") + float(summ)
    count_paid = data_set.get("count_paid") + 1

    updated_data = {"user_id": id, "money": new_money, "count_paid": count_paid}
    conf = await update_user(updated_data)

    if conf:
        await bot.send_message(admin_id, f"Customer's account {id} replenished, shared:  {new_money} $.")
        await bot.send_message(mes_id, f"Your account has been topped up with {summ} $.")
        await bot.answer_callback_query(callback_query.id)
        return
    else:
        await bot.send_message(admin_id, f"Replenishment error.")
        await bot.answer_callback_query(callback_query.id)
        return
####





#### Push /stat ####
@dp.message(Command("stat"))
async def get_stat_user(message: types.Message):

    await typing(message)

    if await paranoia_mode(message):
        return

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return
    
    language = data.get("language")
    data = await read_stat_for_user_id(id)

    if not data:
        await message.answer("Данных еще нет" if language == "ru" else "There is no data yet", parse_mode="HTML")
        return

    all_static = []
    number = 0
    all_static.append(["№", "№", "username table stat", "time", "use model", "sesion token/img/min", "price 1 tok/img/min", "total_price", "id telegram"]) # First a names row
    
    for it in data:
        number += 1
        id_table = it.get("id")
        username_table_stat = it.get("user_id")
        time = it.get("time")
        use_model = it.get("use_model")
        sesion_token = it.get("sesion_token")
        price_1_tok = it.get("price_1_tok")
        total_price = it.get("total_price")


        all_static.append([number, id_table, username_table_stat, time, use_model, sesion_token, price_1_tok, total_price, id]) # added user data

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()


    # csv file to download
    file_name = f"User-statistic-{str(random.randint(30, 40))}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    except:
        logger_bot.error(f"Error sending documentb User stat")
        await message.answer("Ошибка сбора статистики" if language == "ru" else "Statistics collection error", parse_mode="HTML")




# MENU: PRICES:
@dp.message(Command('price'))
async def get_prices(message: types.Message):
    await typing(message)

    if await paranoia_mode(message):
        return

    prices = '''

    OpenAI language model 1 million tokens in $:
        'gpt-5': 13.5,
        'gpt-5-chat-latest': 13.5,
        'gpt-5-mini': 2.7,
        'gpt-5-nano': 0.54,
        'gpt-4.1': 12,
        'gpt-4.1-mini': 2.4,
        'o1-pro': 900,
        'gpt-4.1-nano': 0.6,
        'gpt-4.5-preview': 270,
        'o1': 90,
        'o3-pro': 120,
        'o3': 12,
        'o1-preview': 90,
        'o1-mini': 6.6,
        'o3-mini': 6.6,
        'o4-mini': 6.6,
        'chatgpt-4o-latest': 24,
        'gpt-4o': 24,
        'gpt-4o-2024-05-13': 24,
        'gpt-4o-2024-08-06': 15,
        'gpt-4o-mini': 1.8, # no vision
        'gpt-4o-mini-2024-07-18': 1.8, # no vision
        'gpt-4-turbo-2024-04-09': 48,

    The language model from Google is 1 million in $:
        'gemini-2.5-pro': 13.5,
        'gemini-2.5-flash': 3.36,
        'gemini-2.5-flash-lite-preview-06-17': 0.6,
        'gemini-2.0-flash': 0.6,
        'gemini-2.0-flash-lite': 0.45,
        'gemini-1.5-pro-latest': 3.75,
        'gemini-1.5-flash-latest': 0.225,
        'gemini-1.5-flash-8b': 0.5,
    
    The language model from Elon Musk Grok is 1 million in $:
        'grok-3-latest': 21.6,
        'grok-3-fast-latest': 36, 
        'grok-3-mini-latest': 0.96,
        'grok-3-mini-fast-latest': 5.52,
        'grok-vision-beta': 24,
        'grok-2-vision-latest': 14.4,
        'grok-2-latest': 14.4,
        'grok-beta': 24,

    The language model from Anthropic is 1 million in $:
        'claude-opus-4-latest': 21.6,
        'claude-sonnet-4-latest': 21.6,
        'claude-3-7-sonnet-latest': 21.6,
        'claude-3-5-sonnet-latest': 21.6,
        'claude-3-5-haiku-latest': 5.76,
        'claude-3-opus-latest': 108,
        'claude-3-sonnet-20240229': 21.6,
        'claude-3-haiku-20240307': 1.8,

    Generating images for one in $:
        'dall-e-3-1024': 0.048,
        'dall-e-3-1792': 0.096,
        'dall-e-3-hd-1024': 0.096,
        'dall-e-3-hd-1792': 0.144,
        'dall-e-2-1024': 0.024,
        'dall-e-2-512': 0.0216,
        'dall-e-2-256': 0.0192,

    Voice generation of 1M characters in $:
        'tts-1': 18,
        'tts-1-hd': 36,
        'gpt-4o-mini-tts': 15.12,

    Transcription from audio to text min. in $:
        'whisper-1': 0.0072,

    '''

    await message.answer(prices, parse_mode="HTML")




#### Push /help ####
@dp.message(Command("help"))
async def help(message: types.Message):
    await typing(message)

    if await paranoia_mode(message):
        return
    
    await message.answer(f"Description and instructions are here - https://github.com/shliamb/AI-API-instruction", parse_mode="HTML")





















##### ADMIN ##############
#                        #
#### Push /ADMIN MENU ####
@dp.message(Command("admin"))
async def admin_main_menu(message: types.Message):
    await typing(message)

    id = user_id(message)

    if id != IS_ADMIN:
        #await message.answer(f"Sorry, access is denied.")
        return

    admin_menu_text = (
        f"<b>🎛 ADMIN MENU:</b>\n\n"
        f"<b>📊 STATISTICS:</b>\n"
        f"        Info Users – /allUs\n\n"
        f"<b>📝 LOGS:</b>\n"
        f"        Get logs – /logs\n\n"
        f"<b>🗳 BACKUP & RESTORE:</b>\n"
        f"        Backup DB – /bupDb\n"
        f"        Restore DB – /resDb\n"
        f"        Create Tab DB – /crTabDb\n"
        f"        Down users – /dnlUsers\n"
        f"        Restore Users – /resUs\n\n"
        f"<b>🗑 CLEAR:</b>\n"
        f"        Stat Tab DB – /dStat\n"
        f"        Logs – /dLogs\n"
        f"        All Tabs DB – /allDel\n\n"
        #f"        Get an exel – /stat\n\n"
        f"<b>🧪 SPECIAL:</b>\n"
        f"        Paranoi mode – /para\n"
    )

    await message.answer(admin_menu_text, parse_mode="HTML")





#### Push /PARANOIA_MODE ####
@dp.message(Command("para"))
async def admin_main_menu(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return
    
    global PARANOIA_MODE
    PARANOIA_MODE = False if PARANOIA_MODE else True
    await message.answer("Paranoia mode is enable" if PARANOIA_MODE else "Paranoia mode is disabled", parse_mode="HTML")
    



#### Push /Create Tabs to DB ####
@dp.message(Command("crTabDb"))
async def create_tabs_to_db(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return
    
    if not create_tables_in_db():
        await message.answer("Error create tables", parse_mode="HTML")
    else:
        await message.answer("Adding tables is done!", parse_mode="HTML")
    



# Admin BackupDB
@dp.message(Command("bupDb"))
async def backup(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    confirmation = backup_db() # - резервная копия
    if confirmation:
        await message.answer("The backup copy of the database was created successfully and is presented below. The 3 latest versions are saved in the working folder, the rest are deleted.")
    else:
        await message.answer("Error creating a backup copy of the database.")

    await asyncio.sleep(0.5)

    data_folder = Path("./backup_db/")

    files = [entry for entry in data_folder.iterdir() if entry.is_file()] # Получаем список всех файлов в директории

    sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True) # Сортируем список файлов по дате изменения (от новых к старым)

    for file_to_delete in sorted_files[3:]: # Оставляем последние 3 файла, удаляем остальные
        os.remove(file_to_delete)
    logger_bot.info("Remove all file DB, saved 3 latest files.")

    last_downloaded_file = sorted_files[0] if sorted_files else None   # Последний скачанный файл будет первым в отсортированном списке (новейшим) (адрес)
    logger_bot.info("Download last DB file.")

    await message.bot.send_document(chat_id=message.chat.id, document=types.input_file.FSInputFile(last_downloaded_file))




# Fast Delete All Tables in DB:
@dp.message(Command('allDel'))
async def delete_all_tables_in_db_admin(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    if await drop_all_tables_and_reset_schema():
        await bot.send_message(message.chat.id, "All tables have been deleted successfully.")
    else:
        await bot.send_message(message.chat.id, "Error deleting all tables.")



# Admin get statistic
@dp.message(Command("allUs"))
async def get_admin_stat(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    data = await read_users()

    if not data:
        await message.answer("There is no data yet", parse_mode="HTML")
        return

    all_static = []
    number = 0
    all_static.append(["№", "user_id", "name", "full_name", "first_name", "last_name", "count_paid", "money", "notifications", "last_visit"]) 
    
    for it in data:
        number += 1
        user_id_tel = it.get("user_id")
        name = it.get("name")
        full_name = it.get("full_name")
        first_name = it.get("first_name")
        last_name = it.get("last_name")
        count_paid = it.get("count_paid")
        money = round(it.get("money"), 2)
        notifications = it.get("notifications")
        last_visit = it.get("last_visit")


        all_static.append([number, user_id_tel, name, full_name, first_name, last_name, count_paid, money, notifications, last_visit]) # added user data

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()


    # csv file to download
    file_name = f"Admin-statistic-{str(random.randint(30, 40))}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    except:
        logger_bot.error(f"Error sending document Admin stat")



# Admin submenu download log
@dp.message(Command("logs"))
async def admin_get_log(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    data_folder = Path(PATH_LOGS)
    empts = True
    for entry in data_folder.iterdir():
        if entry.is_file() and entry.stat().st_size > 0:  # Проверяем, что файл не пустой
            file_path = str(entry.absolute())  # Получаем абсолютный путь
            try:
                await bot.send_document(
                    chat_id=message.from_user.id,
                    document=types.input_file.FSInputFile(file_path)
                )
                empts = False
                await asyncio.sleep(0.5)
            except Exception as e:
                logger_bot.error(f"Error sending file log: {file_path}: {e}")
    if empts:
        await bot.send_message(message.chat.id, "There are no log files or they are empty")




# Admin clear logs /dLogs
@dp.message(Command("dLogs"))
async def admin_clear_log(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    data_folder = Path(PATH_LOGS)
    empts = True
    for entry in data_folder.iterdir():
        if entry.is_file() and entry.stat().st_size > 0:  # Проверяем, что файл не пустой
            file_path = str(entry.absolute())  # Получаем абсолютный путь
            try:
                with open(file_path, 'w'):
                    pass
                await bot.send_message(message.chat.id, f"The '{file_path}' file has been clearing.")
                empts = False
                await asyncio.sleep(0.5)
            except Exception as e:
                logger_bot.error(f"Error clearing file log: {file_path}: {e}")
        
    if empts:
        await bot.send_message(message.chat.id, "There are no log files or they are empty")










# Admin delete_stat_table /dStat
@dp.message(Command("dStat"))
async def admin_delete_stat_table(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    if not await delete_stat_table():
        logger_bot.error("Error delete_stat_table !")
        return

    await message.answer("Table Statistic of DB is deleted", parse_mode="HTML")









# Admin Restore DB
class Restor_db(StatesGroup):
    load_db = State()


# Push button - restore
@dp.message(Command('resDb'))
async def restore_db_admin(message: types.Message, state: FSMContext):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return
    
    await bot.send_message(message.chat.id, "Attach and send the necessary copy of the database for recovery.", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(Restor_db.load_db)



@dp.message(Restor_db.load_db)
async def load_a_base(message: Message, state: FSMContext):

    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    if not isinstance(message.document, types.Document):
        await message.answer("Вы передали не документ.")
        return

    file_extension = message.document.file_name.split('.')[-1]
    allowed_extensions = ['sql']

    if file_extension not in allowed_extensions:
        await message.answer("Вы передали файл не sql расширения.")
        return    

    file_name = f"uploaded-db-restore.sql"
    file_path = f"{DOWNLOAD}{file_name}"
    await bot.download(message.document, file_path) # То что прикрепили и отправили, скачивается в папку с новым именем

    await bot.session.close()
    await dp.storage.close()

    confirmation = restore_db(file_path) # Восстановелние базы

    if confirmation == True:
        await message.answer("Восстановление базы данных прошло успешно.")
    else:
        await message.answer("При восстановлении базы данных, что то пошло не так.")

    await state.clear()






# Admin Restore Users to DB in Json
class Restore_json(StatesGroup):
    load_json = State()

# Resore OLD users to DB:
@dp.message(Command('resUs'))
async def restore_old_users_admin(message: types.Message, state: FSMContext):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    await bot.send_message(message.chat.id, "Attach and send the necessary json file for recovery Users to DB.", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(Restore_json.load_json)


@dp.message(Restore_json.load_json)
async def load_json_users_to_db(message: Message, state: FSMContext):
    await typing(message)
    id = user_id(message)
    
    if not isinstance(message.document, types.Document):
        await message.answer("It's not a documents")
        return

    file_extension = message.document.file_name.split('.')[-1]
    allowed_extensions = ['json']

    if file_extension not in allowed_extensions:
        await message.answer("You have sent a non-json extension file.")
        return 

    file_name = f"uploaded-json-restore-users.json"
    file_path = f"{DOWNLOAD}{file_name}"
    await bot.download(message.document, file_path)

    await bot.session.close()
    await dp.storage.close()


    res_update_db = await restore_users_to_db(file_path)

    if res_update_db:
        await message.answer(f"Results of adding regular Users to DB:\n{res_update_db}")
    else:
        await message.answer(f"Error of adding regular Users to DB:\n{res_update_db}")

    await state.clear()





# Get_on_json_old_users:
@dp.message(Command('dnlUsers'))
async def get_on_json_old_users(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != IS_ADMIN:
        return

    name_file = await get_json_old_users()
    if not name_file:
        await message.answer(f"No users found with money > {MONEY_TO_START}$")
        return

    if os.path.exists(name_file) and os.path.getsize(name_file) > 0:
        await bot.send_document(message.chat.id, document=types.input_file.FSInputFile(name_file))
    else:
        await bot.send_message(message.chat.id, "File (name_file) is empty or missing.")        













# main def polling
async def main_bot() -> None:
    await dp.start_polling(bot, skip_updates=False) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей


# Start polling
if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except Exception as e:
        logger_bot.error(f"An error occurred: {e}.")
        print(f"An error occurred: {e}.")














    # chat_id = callback_query.message.chat.id
    # message_id = callback_query.message.message_id