from keys import USER_DB, PASSWORD_DB, DB_NAME
from config import MONEY_TO_START, HOST
from setup_config_logger import setup_logger
logger_db = setup_logger('db', '/log/db.log')
import asyncpg
# import json
# import asyncio
import uuid



# Asinc onnection to DB:
async def get_connection():
    connection = await asyncpg.connect(
        host=HOST, # app_postgres  localhost  имя контейнера
        database=DB_NAME,
        user=USER_DB,
        password=PASSWORD_DB
    )
    return connection






#### USERS TABLE: ####
######################

# Add user:
async def add_user(user_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None 

    # user_id = user_data.get("user_id")
    # counts_api = user_data.get("counts_api")
    # if user_id is not None or counts_api is not None:
    #     logger_db.error("Error add_user: Not enough data") !!!!!!!!!
    #     return False


    for key, value in user_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO telegram ({keys}) VALUES ({nums})
            ''', 
            *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_user: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# Read user ID:
async def read_user(user_id):
    connection = None
    try:
        #logger_db.info(f"INFO: Reade user_id:{user_id}")

        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM telegram WHERE user_id = $1;
            ''',
            user_id,
        )

        if not result:
            return {}

        return dict(*result)
    
    except Exception as e:
        logger_db.error(f"Error read_user: {e}")
        return False

    finally:
        if connection:
            await connection.close()


# # import json
# data = asyncio.run(read_user(1666495))
# print(data)

# # for key, value in data.items():
# #     #json_list = n.get("list_access_id")
# #     if key == "list_access_id":
# #         print(json.loads(value))
# print(data.get("list_access_id"))




# Read ALL users:
async def read_users():
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM telegram;
            '''
        )

        if not result:
            return []

        users = []
        for rec in result:
            users.append(dict(rec))
            
        return users
    
    except Exception as e:
        logger_db.error(f"Error read_users: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Update user:
async def update_user(user_data):
    keys_list, values_list, i, connection = [], [], 1, None

    user_id = user_data.get("user_id")
    if not user_id:
        logger_db.error("Error update_user: Not enough data") 
        return False

    for key, value in user_data.items():
        if key != "user_id":
            keys_list.append(f"{key} = ${i}")
            values_list.append(value) #user_data[key])
            i += 1

    update_string = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    values_list.append(user_id)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            UPDATE telegram SET {update_string} WHERE user_id = ${i};
            ''',
            *values_list
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error update_user: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()







#### ACCOUNT API ACCESS TABLE: ####
###################################

# Add ACCOUNT:
async def add_account(account_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None 

    access_id = account_data.get("access_id")
    api_key = account_data.get("api_key")
    api_value = account_data.get("api_value")
    user_id_telegram = account_data.get("user_id_telegram")
    if not access_id or not api_key or not api_value or not user_id_telegram:
        logger_db.error("Error update_account: Not enough data")
        #print("Error update_account: Not enough data")
        return False

    for key, value in account_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO account_api_access ({keys}) VALUES ({nums})
            ''', 
            *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_account: {e}")
        #print(f"Error add_account: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()



# Read ACCOUNT for access_id:
async def read_account_access_id(access_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM account_api_access WHERE access_id = $1;
            ''',
            access_id,
        )

        if not result:
            return {}

        return dict(*result)
    
    except Exception as e:
        logger_db.error(f"Error read_account_access_id: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Read ACCOUNTS for user_id_telegram:
async def read_accounts_user_id(user_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM account_api_access WHERE user_id_telegram = $1;
            ''',
            user_id,
        )

        if not result:
            return []

        accounts = []
        for record in result:
            accounts.append(dict(record))
        return accounts
    
    except Exception as e:
        logger_db.error(f"Error read_accounts_user_id: {e}")
        return False

    finally:
        if connection:
            await connection.close()


# print(asyncio.run(read_accounts_user_id(1666495)))

# Update account:
async def update_account(account_data):
    keys_list, values_list, i, connection = [], [], 1, None

    access_id = account_data.get("access_id")
    if not access_id:
        logger_db.error("Error update_account: Not enough data") 
        return False

    for key, value in account_data.items():
        if key != "access_id":
            keys_list.append(f"{key} = ${i}")
            values_list.append(value) #user_data[key])
            i += 1

    update_string = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    values_list.append(access_id)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            UPDATE account_api_access SET {update_string} WHERE access_id = ${i};
            ''',
            *values_list
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error update_account: {e}")
        #print(f"Error update_account: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# Dellete account:
async def del_account(access_id):
    connection = None

    if not access_id:
        logger_db.error("Error del_account: Where is access_id?") 
        return False

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            DELETE FROM account_api_access WHERE access_id = $1;
            ''',
            access_id
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error del_account: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()








#### STATISTIC TABLE: ####
##########################

# Add record stat:
async def add_record_stat(stat_data):
    keys_list, values_list, num_list, i, connection = [], [], [], 1, None 

    user_id = stat_data.get("user_id")
    time = stat_data.get("time")
    access_id = stat_data.get("access_id")
    if not user_id or not time or not access_id:
        logger_db.error("Error add_record_stat: Not enough data") 
        return False

    for key, value in stat_data.items():
        keys_list.append(key)
        values_list.append(value)
        num_list.append(f"${i}")
        i += 1

    keys = ", ".join(keys_list) # <-- в строку, а * распоковывает поотдельности
    nums = ", ".join(num_list)

    try:
        connection = await get_connection()
        await connection.execute(
            f'''
            INSERT INTO statistics ({keys}) VALUES ({nums})
            ''', 
            *values_list # Оператор распоковки *
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error add_record_stat: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# Read stat for user_id:
async def read_stat_for_user_id(user_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM statistics WHERE user_id = $1;
            ''',
            user_id,
        )

        if not result:
            return []

        list_stat = []
        for record in result:
            list_stat.append(dict(record))
        return list_stat
    
    except Exception as e:
        logger_db.error(f"Error read_stat_for_user_id: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Read stat for access_id:
async def read_stat_for_access_id(access_id):
    connection = None
    try:
        connection = await get_connection()
        result = await connection.fetch(
            '''
                SELECT * FROM statistics WHERE access_id = $1;
            ''',
            access_id,
        )

        if not result:
            return []

        list_stat = []
        for record in result:
            list_stat.append(dict(record))
        return list_stat
    
    except Exception as e:
        logger_db.error(f"Error read_stat_for_access_id: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Delete_stat_table:
async def delete_stat_table():
    connection = None

    try:
        connection = await get_connection()
        await connection.execute(
            '''
            TRUNCATE TABLE statistics;
            '''
        )
        return True
    
    except Exception as e:
        logger_db.error(f"Error delete_stat_table: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()







def extended_encoder(obj):
    '''Кастомный сериализатор для нестандартных типов данных'''
    if isinstance(obj, uuid.UUID):  # Обрабатываем UUID
        return str(obj)
    
    # elif isinstance(obj, datetime):  # Обрабатываем дату/время
    #     return obj.isoformat()
    
    elif hasattr(obj, '__dict__'):  # Обрабатываем объекты с атрибутами
        return obj.__dict__
    
    else:
        return obj
    
    # raise TypeError(f"Object of type {type(obj)} is not JSON serializable")





async def json_old_users():
    '''Собираю всех пользователей, кто хоть раз платил и у кого счет больше чем тестовый'''
    connection = None
    try:
        connection = await get_connection()
        
        # Выполняем запрос с LEFT JOIN
        records = await connection.fetch(
            '''
            SELECT 
                t.*,
                a.*
            FROM 
                telegram t
            LEFT JOIN 
                account_api_access a ON t.user_id = a.user_id_telegram
            WHERE 
                t.money > $1 OR t.count_paid > $2
            ''',
            MONEY_TO_START, 0
        )
        
        if not records:
            logger_db.warning("No users found with money > %s$", MONEY_TO_START)
            return []



        users = {}
        account_fields = {"access_id", "api_key", "api_value", "is_active", "user_id_telegram"}  # Поля аккаунта

        for record in records:

            user_id = dict(record)["user_id"]# дату пропускает date, потому, лишь для user_id

            accounts_data = {}

            if user_id not in users:
                users[user_id] = {"telegram_data": {}, "account_data": []}

                for key, value in record.items():

                    if value is None:
                        continue

                    if key in account_fields:
                        accounts_data[key] = extended_encoder(value)
                    else:    
                        users[user_id]["telegram_data"][key] = extended_encoder(value)

                if accounts_data:
                    users[user_id]["account_data"].append(accounts_data)
            else:


                for key, value in record.items():

                    if value is None:
                        continue

                    if key in account_fields:
                        accounts_data[key] = extended_encoder(value)

                if accounts_data:
                    users[user_id]["account_data"].append(accounts_data)

        return list(users.values())
        # return users
    
    except Exception as e:
        logger_db.error(f"Error in json_old_users: {e}", exc_info=True)
        return []
    finally:
        if connection:
            await connection.close()

# res = asyncio.run(json_old_users())
# print(res)





















