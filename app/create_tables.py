from get_keys import USER_DB, PASSWORD_DB, DB_NAME
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO, filename='./log/api.log')
import psycopg2


# Create TABLES:
def create_tables_in_db():

    try:
        # Conect to db:                   имя контейнера app_postgres   localhost
        connection = psycopg2.connect(host="localhost", database=DB_NAME, user=USER_DB, password=PASSWORD_DB)
        
        cursor = connection.cursor()

 
 
        create_table_users = '''
        CREATE TABLE IF NOT EXISTS users (
            -- User data
            username VARCHAR(50) PRIMARY KEY,           --(Username пользователя, для идентификации в API)
            appkey UUID,                                --(UUID в качестве API Key)
            is_failed INTEGER DEFAULT 0,                --(Неудачные попытки доступа)
            is_block BOOLEAN DEFAULT FALSE,             --(Заблокирован ли пользователь из-за колл. не верных вводов.)
            date_block TIMESTAMP,                       --(Дата и время блокировки, для отсчета времени блокировки)
            date_last_activ TIMESTAMP,                  --(Дата последней активности)
            time_zone VARCHAR(10), 
            language VARCHAR(10),
            paid INTEGER DEFAULT 0,                     --(Колличество оплат)
            money FLOAT,                                --(Денег на счету)
            money_currency VARCHAR(50) DEFAULT "$",     --(Валюта)
            notifications BOOLEAN,

            -- Telegram
            id BIGINT UNIQUE NOT NULL,                  --(Телеграмм id)
            name VARCHAR(50),
            full_name VARCHAR(50),
            first_name VARCHAR(50),
            last_name VARCHAR(50)
        );
        CREATE INDEX sid_username ON users(username);
        CREATE INDEX sid_appkey ON users(appkey);
        CREATE INDEX sid_is_failed ON users(is_failed);
        CREATE INDEX sid_is_block ON users(is_block);
        CREATE INDEX sid_id ON users(id);
        '''
        cursor.execute(create_table_users)


        # Нужно будет очисчать таблицу от старых сессий, в постгресс есть встроенная функция - партиционирования
        create_table_statistics = '''
        CREATE TABLE IF NOT EXISTS statistics (
            id BIGINT PRIMARY KEY,                      --(Телеграмм id)
            time TIMESTAMP,
            use_model VARCHAR(100),                     --(Используемая модель в сессии)
            sesion_token FLOAT,
            price_1_tok FLOAT,
            total_price FLOAT,

            username_table_stat VARCHAR(50),
            
            FOREIGN KEY (username_table_stat) REFERENCES users(username)
        );
        '''
        cursor.execute(create_table_statistics)


        # Saving changes:
        connection.commit()
        print("Adding tables is done!")
        logging.info("Adding tables is done!")

    except Exception as error:
        print("Error:", error)
        logging.error("Error create tables:", error)
    finally:

        # Closing the cursor and database connection
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()



create_tables_in_db()





# VARCHAR(n) - строковый тип данных ограничение n, TEXT - строковый тип данных ограничение в 1Гб.
# iuser_id INTEGER SERIAL PRIMARY KEY , тут SERIAL - означает, что каждый последующее число в строке будет само увеличиваться..
# Если ячейка является первичным ключем, то она автоматически добавленна в индекс, CONSTRAINT unique_user_id UNIQUE (user_id)  -- Создание уникального ограничения также создает индекс
# INTEGER  BIGINT block BOOLEAN NOT NULL DEFAULT FALSE  INTEGER  VARCHAR(100) NOT NULL UNIQUE UNIQUE
# time_zone TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# UNIQUE - автоматом индексируются
# INDEX idx_name (name)  -- Создание обычного индекса на колонке name



# url VARCHAR(800),
# in_date TIMESTAMP,
# last_ping TIMESTAMP,
# ip VARCHAR(500),
# mouse BOOLEAN,
# battery FLOAT,
# canvas VARCHAR(300),
# processors INTEGER,
# ram INTEGER,
# webgl VARCHAR(500),
# touch INTEGER,
# useragent VARCHAR(500),
# language VARCHAR(10),
# platform VARCHAR(50),
# screenResolution VARCHAR(50),
# timezoneoffset INTEGER,
# plugins VARCHAR(150),
# networkinfo VARCHAR(1000),
# location VARCHAR(500),