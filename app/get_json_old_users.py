# Base:
from worker_db import json_old_users
from config import PATH_JSON_USERS, LOG_CONFIG_DB, setup_logger
# import asyncio
import os
import json
import uuid
from datetime import datetime
logger_db = setup_logger('db', LOG_CONFIG_DB)






def extended_encoder(obj):
    '''Кастомный сериализатор для нестандартных типов данных'''
    if isinstance(obj, uuid.UUID):  # Обрабатываем UUID
        return str(obj)
    
    elif isinstance(obj, datetime):  # Обрабатываем дату/время
        return obj.isoformat()
    
    elif hasattr(obj, '__dict__'):  # Обрабатываем объекты с атрибутами
        return obj.__dict__
    
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")






async def get_json_old_users():
    '''Собирает из базы всех пользователей кто хоть раз платил или счет больше тестовой суммы'''

    try:
        users_data = await json_old_users()

        if not users_data:
            return False

        list_users_data = []
        for rec in users_data:
            telegram_data = rec.get("telegram_data")
            account_data = rec.get("account_data")

            # Преобразуем строку JSON в настоящий список
            list_access_id = telegram_data.get("list_access_id")
            if list_access_id and isinstance(list_access_id, str):
                try:
                    telegram_data['list_access_id'] = json.loads(list_access_id)
                except json.JSONDecodeError:
                    telegram_data['list_access_id'] = str(list_access_id)

            new_rec_user = {**telegram_data, "account_data": account_data}
            list_users_data.append(new_rec_user)

        #print(list_users_data)
        # Создаем имя файла с текущей датой-временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{PATH_JSON_USERS}users_data_{timestamp}.json"
        
        # Полный путь к файлу в рабочей директории
        filepath = os.path.join(os.getcwd(), filename)
        
        # Сохраняем с обработкой специальных типов
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                users_data, 
                f, 
                ensure_ascii=False, 
                indent=4,
                default=extended_encoder
            )
        
        return filepath

    except Exception as e:
        logger_db.error(f"Error save file to JSON: {e}")
        return False
    
# print(asyncio.run(get_json_old_users()))