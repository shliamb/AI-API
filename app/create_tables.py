from keys import USER_DB, PASSWORD_DB, DB_NAME
from config import HOST
import psycopg2
from setup_config_logger import setup_logger
logger_db = setup_logger('db', '/log/db.log')



# Create TABLES:
def create_tables_in_db():

    try:
        # Conect to db:
        connection = psycopg2.connect(host=HOST, database=DB_NAME, user=USER_DB, password=PASSWORD_DB)
        
        cursor = connection.cursor()


        # Account Telegram: 
        create_table_telegram  = '''
        CREATE TABLE IF NOT EXISTS telegram  (

            user_id BIGINT PRIMARY KEY,
            name VARCHAR(50),
            full_name VARCHAR(100),
            first_name VARCHAR(50),
            last_name VARCHAR(50),

            counts_api INTEGER NOT NULL,                        -- Колличество доступов к АПИ
            list_access_id VARCHAR(300),                        -- Список access_id пользователя
            last_visit TIMESTAMP,
            time_zone VARCHAR(32), 
            language VARCHAR(10),
            count_paid INTEGER DEFAULT 0,                       -- Колличество оплат
            money FLOAT,
            block_user BOOLEAN DEFAULT FALSE,
            god_user BOOLEAN DEFAULT FALSE,                     -- Пользователь, на котором нет проверки денег - для себя и своих проектов
            notifications BOOLEAN
        );
        CREATE INDEX sid_user_id ON telegram(user_id);
        CREATE INDEX sid_block ON telegram(block_user);
        CREATE INDEX sid_notifications ON telegram(notifications);
        CREATE INDEX sid_counts_account_api ON telegram(counts_api);
        CREATE INDEX sid_list_access_id ON telegram(list_access_id);
        '''
        cursor.execute(create_table_telegram)


        # Account API Access:
        # Пользователь может имень много доступов, но не более - count_account_api
        # access_id - главный идентификатор доступа
        create_table_account_api_access  = '''
        CREATE TABLE IF NOT EXISTS account_api_access  (

            access_id UUID PRIMARY KEY,                 -- UUID access_id
            api_key VARCHAR(100) NOT NULL,              -- строка 'appkey'
            api_value UUID UNIQUE NOT NULL,             -- UUID value

            is_active BOOLEAN DEFAULT TRUE,             -- Для блокировки
            access_type VARCHAR(20),                    -- "read-only", "full-access" и т.д.
            last_visit TIMESTAMP,                       -- Дата последней активности

            user_id_telegram BIGINT NOT NULL,           -- user_id telegram 

            FOREIGN KEY (user_id_telegram) REFERENCES telegram(user_id) ON DELETE CASCADE
        );
        CREATE INDEX sid_access_id ON account_api_access(access_id);
        CREATE INDEX sid_api_key ON account_api_access(api_key);
        CREATE INDEX sid_is_api_value ON account_api_access(api_value);
        CREATE INDEX sid_is_access_type ON account_api_access(access_type);
        '''
        cursor.execute(create_table_account_api_access)


        # Table Statistic Request to API:
        # Нужно партиционирование, или в админке кнопка - очистка таблицы
        create_table_statistics = '''
        CREATE TABLE IF NOT EXISTS statistics (
            id SERIAL PRIMARY KEY,                      -- Просто порядковый номер
            user_id BIGINT NOT NULL,                    -- Телеграмм id
            time TIMESTAMP NOT NULL,
            use_model VARCHAR(100),                     -- Используемая модель в сессии
            sesion_token FLOAT,
            price_1_tok FLOAT,
            total_price FLOAT,

            access_id UUID NOT NULL,
            FOREIGN KEY (access_id) REFERENCES account_api_access(access_id) ON DELETE CASCADE
        );
        '''
        cursor.execute(create_table_statistics)


        # Saving changes:
        connection.commit()
        #print("Adding tables is done!")
        logger_db.info("Adding tables is done!")
        return True

    except Exception as error:
        # print("Error:", error)
        logger_db.error("Error create tables:", error)
        return False

    finally:

        # Closing the cursor and database connection
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()



# create_tables_in_db()





# VARCHAR(n) - строковый тип данных ограничение n, TEXT - строковый тип данных ограничение в 1Гб.
# iuser_id INTEGER SERIAL PRIMARY KEY , тут SERIAL - означает, что каждый последующее число в строке будет само увеличиваться..
# Если ячейка является первичным ключем, то она автоматически добавленна в индекс, CONSTRAINT unique_user_id UNIQUE (user_id)  -- Создание уникального ограничения также создает индекс
# INTEGER  BIGINT block BOOLEAN NOT NULL DEFAULT FALSE  INTEGER  VARCHAR(100) NOT NULL UNIQUE UNIQUE
# time_zone TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# UNIQUE - автоматом индексируются
# INDEX idx_name (name)  -- Создание обычного индекса на колонке name