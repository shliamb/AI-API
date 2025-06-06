from keys import USER_DB, PASSWORD_DB, DB_NAME
import asyncpg
# import asyncio
import logging
#logging.basicConfig(format='%(message)s', level=logging.INFO) # filename='./log/api.log',
logging.basicConfig(format='%(message)s', level=logging.INFO)


# Asinc onnection to DB:
async def get_connection():
    connection = await asyncpg.connect(
        host="localhost", # app_postgres  localhost  имя контейнера
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

    user_id = user_data.get("user_id")
    counts_api = user_data.get("counts_api")
    if not user_id or not counts_api:
        logging.error("Error add_user: Not enough data") 
        return False


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
        logging.error(f"Error add_user: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# Read user ID:
async def read_user(user_id):
    connection = None
    try:
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
        logging.error(f"Error read_user: {e}")
        return False

    finally:
        if connection:
            await connection.close()



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
        logging.error(f"Error read_users: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Update user:
async def update_user(user_data):
    keys_list, values_list, i, connection = [], [], 1, None

    user_id = user_data.get("user_id")
    if not user_id:
        logging.error("Error update_user: Not enough data") 
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
        logging.error(f"Error update_user: {e}")
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
        logging.error("Error update_account: Not enough data") 
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
        logging.error(f"Error add_account: {e}")
        print(f"Error add_account: {e}")
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
        logging.error(f"Error read_account_access_id: {e}")
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
        logging.error(f"Error read_accounts_user_id: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Update account:
async def update_account(account_data):
    keys_list, values_list, i, connection = [], [], 1, None

    access_id = account_data.get("access_id")
    if not access_id:
        logging.error("Error update_account: Not enough data") 
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
        logging.error(f"Error update_account: {e}")
        print(f"Error update_account: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()


# Dellete account:
async def del_account(access_id):
    connection = None

    if not access_id:
        logging.error("Error del_account: Where is access_id?") 
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
        logging.error(f"Error del_account: {e}")
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
        logging.error("Error add_record_stat: Not enough data") 
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
        logging.error(f"Error add_record_stat: {e}")
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
        logging.error(f"Error read_stat_for_user_id: {e}")
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
        logging.error(f"Error read_stat_for_access_id: {e}")
        return False

    finally:
        if connection:
            await connection.close()



# Delete_stat_table:
async def delete_stat_table():

    try:
        connection = await get_connection()
        await connection.execute(
            '''
            TRUNCATE TABLE statistics;
            '''
        )
        return True
    
    except Exception as e:
        logging.error(f"Error delete_stat_table: {e}")
        return False
    
    finally:
        if connection:
            await connection.close()