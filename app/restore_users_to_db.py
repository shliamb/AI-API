# Base:
from worker_db import add_user, add_account
# import asyncio
import json
import uuid
from datetime import datetime
from setup_config_logger import setup_logger
logger_db = setup_logger('db', '/log/db.log')








def datetime_to_db(value):
    '''to  datetime.datetime(2024, 10, 14, 0, 8, 38)'''
    try:
        return datetime.fromisoformat(value)  # Пробуем распарсить
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  # Если не ISO-формат, пробуем другой формат



async def restore_users_to_db(file_path):

    """Импортирует постоянных клиентов из JSON, добавляет или обновляет в БД."""

    qty_add_usr = 0
    err_add_usr = 0

    qty_met_pay = 0
    err_met_pay = 0



    # Открытие файла и в файл:
    with open(file_path, "r") as file:
        users_json = json.load(file) # В dict

    # Списки для обработки данных:
    list_keys_date = ["last_visit"]
    list_keys_list = ["list_access_id"]
    list_key_uuid = ["access_id", "api_value"]



    for record in users_json:
        user_records = record.get("telegram_data")


        # Users Table:
        try:
            clear_data_user = {} 
            for key, value in user_records.items():
                if key in list_keys_date:
                    clear_data_user[key] = datetime_to_db(value)
                elif key in list_keys_list:
                    clear_data_user[key] = json.dumps(value)
                else:
                    clear_data_user[key] = value

            if await add_user(clear_data_user):
                qty_add_usr += 1

        except Exception as err:
            err_add_usr += 1
            logger_db.error(f"Fail update user_id: {clear_data_user.get('user_id')}, reason: {err}")
        


    # Accounts Table:
    for record in users_json:
        accounts_records = record.get("account_data")

        if not accounts_records:
            continue

        try:
            clear_data_account = {}
            one_account = {}
            i = 1
            for account_rec in accounts_records:
                #print(account_rec)

                for key, value in account_rec.items():
                    if key in list_keys_date:
                        one_account[key] = datetime_to_db(value)
                    elif key in list_keys_list:
                        one_account[key] = json.dumps(value)
                    elif key in list_key_uuid:
                        one_account[key] = uuid.UUID(value)
                    else:
                        one_account[key] = value

                clear_data_account[i] = one_account
                one_account = {}
                i += 1

            data_accont = list(clear_data_account.values())
            for data in data_accont:
                if await add_account(data):
                    qty_met_pay += 1

        except Exception as err:
            err_met_pay += 1
            logger_db.error(f"Fail update user_id: {clear_data_account.get('user_id_telegram')}, reason: {err}")


    return {"status": "good", "added users": qty_add_usr, "errors users": err_add_usr, "added accounts": qty_met_pay, "errors accounts": err_met_pay}
    



# print(asyncio.run(restore_users_to_db("./download/uploaded-json-restore-users.json")))











    # except Exception as err:
    #     logging.critical(f"Fail open or handle file: {err}")
    #     return {"status": f"bad: {err}", "added users": qty_add_usr, "errors users": err_add_usr, "added accounts": qty_met_pay, "errors accounts": err_met_pay}


        














        #     try:
        #         if await add_user(data):
        #             qty_add_usr += 1
        #     except Exception:
        #         try:
        #             if await update_user(data):
        #                 qty_add_usr += 1
        #         except Exception as err:
        #             logging.error(f"Fail update user_id: {user_id}, reason: {err}")
        #             err_add_usr += 1

#         # Metods Pay:
#         for metod in metods_pay:
#             try:
#                 if await add_methods_pay(metod):
#                     qty_met_pay += 1
#             except Exception as err:
#                 logging.error(f"Fail update metod pay: {metod}, reason: {err}")
#                 err_met_pay += 1
                # print(f"\nSave User: {user_data}\n\n{user_id}")
                # print(f"last_visit: {type(user_data.get('last_visit'))}")
                # print(f"list_access_id: {type(user_data.get('list_access_id'))}")
                    # print(f"\nSave Account: {account_data}\n")
                    # print(f"access_id: {type(user_data.get('access_id'))}")


















# last_visit': datetime.datetime(2025, 6, 8, 16, 5, 31, 843190)

# metods_pay = [
#     {
#         'date': datetime.datetime(2024, 10, 14, 0, 8, 38), 
#         'counts': 0, 
#         'use_sbp_transfer': None, 
#         'use_mastercard': None, 
#         'use_visa': None, 
#         'use_mircard': True, 
#         'use_cripto': None, 
#         'use_sms': None, 
#         'use_stars': None, 
#         'use_telegram': None, 
#         'use_digital': None, 
#         'title_method_pay': 'OZON  CARD NUMBER', 
#         'method_pay_ru': 'Переведите на карту банка OZON по номеру карты  2204 2402 7076 3321 из приложения своего банка. На имя Александр В. сумму вводимую ранее.', 
#         'method_pay_en': "Transfer to the OZON Bank card by card number 2204 2402 7076 3321 from your bank's application. In the name of Alexander V. the amount entered earlier."
#     },  
#     {
#         'date': datetime.datetime(2024, 10, 14, 0, 9, 11), 
#         'counts': 0, 
#         'use_sbp_transfer': None, 
#         'use_mastercard': True, 
#         'use_visa': None, 
#         'use_mircard': None, 
#         'use_cripto': None, 
#         'use_sms': None, 
#         'use_stars': None, 
#         'use_telegram': None, 
#         'use_digital': None, 
#         'title_method_pay': 'Jusan', 
#         'method_pay_ru': 'Переведите на карту банка JUSAN по номеру карты  5395 4599 0505 1850 из приложения своего банка. На имя Александр В. сумму вводимую ранее.', 
#         'method_pay_en': "Transfer to a JUSAN Bank card using the card number 5395 4599 0505 1850 from your bank's application. In the name of Alexander V. the amount entered earlier."
# }
# ]