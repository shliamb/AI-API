from keys import user_db, paswor_db
import logging
import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, UsersBase, Statistics
from sqlalchemy import select, insert, update, join, func


# import os
# from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
# user_db, paswor_db = os.environ.get('USER_DB'),  os.environ.get('PASWOR_DB')



async def create_async_engine_and_session():                                # @localhost  # @postgres
    engine = create_async_engine(f"postgresql+asyncpg://{user_db}:{paswor_db}@postgres:5432/my_database") # echo=True - вывод логирования
    async_session = sessionmaker(bind=engine, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_session

#### USER TELEGRAM PROPERTY #### 
# Read User Telegram Data by id
async def get_user_by_id(id):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        # Выполняем запрос на выборку данных пользователя из таблицы UsersTelegram по переданному идентификатору
        query = select(UsersBase).filter(UsersBase.id == id)
        result = await session.execute(query)
        # Получаем первую строку, которая соответствует запросу
        data = result.scalar_one_or_none()  # - это метод SQLAlchemy, который возвращает ровно один результат из результата запроса или None, если запрос не вернул ни одного результата.
        return data or None

# Read User Telegram Data by username
async def get_user_by_username(username):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        # Выполняем запрос на выборку данных пользователя из таблицы UsersTelegram по переданному идентификатору
        query = select(UsersBase).filter(UsersBase.username == username)
        result = await session.execute(query)
        # Получаем первую строку, которая соответствует запросу
        data = result.scalar_one_or_none()  # - это метод SQLAlchemy, который возвращает ровно один результат из результата запроса или None, если запрос не вернул ни одного результата.
        return data or None

# Update User Telegram by ID
async def update_user(id, updated_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = update(UsersBase).where(UsersBase.id == id).values(**updated_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info(f"update_user {id}")
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
    return confirmation


# Update User Telegram by Username
async def update_user_by_username(username, updated_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = update(UsersBase).where(UsersBase.username == username).values(**updated_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info(f"update_user {username}")
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
    return confirmation

# Add User Telegram to DB
async def adding_user(user_data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = insert(UsersBase).values(**user_data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info("adding_user")
        except Exception as e:
            logging.error(f"Failed to add user: {e}")
    return confirmation


#### STATISTICS ####
# Add statistics
async def add_statistic(data):
    async_session = await create_async_engine_and_session()
    confirmation = False
    async with async_session() as session:
        try:
            query = insert(Statistics).values(**data)
            await session.execute(query)
            await session.commit()
            confirmation = True
            logging.info("Add a one statistics line to table")
        except Exception as e:
            logging.error(f"Failed to add statistics: {e}")
    return confirmation


# Read Statistics on id all 30 line
async def get_last_30_statistics(username_table_stat):
    async_session = await create_async_engine_and_session()
    async with async_session() as session:
        query = (
            select(Statistics)
            .filter(Statistics.username_table_stat == username_table_stat)
            .order_by(Statistics.time.desc())  # Сортировка по убыванию даты
            .limit(100)  # Ограничение на количество строк
        )
        result = await session.execute(query)
        data = result.scalars().all()  # Получение всех строк
        return data


# # ADMIN Read all settings and users an id
# async def get_all_stat_admin():
#     async_session = await create_async_engine_and_session()
#     async with async_session() as session:

#         query = (
#             select(UsersTelegram, Settings)
#             .join(Settings)
#         )

#         # for user_telegram, settings in data:
#         #     print("User:", user_telegram.id, user_telegram.is_admin, user_telegram.full_name,\
#         #            user_telegram.name)
#         #     print("Settings:", settings.id, settings.temp_chat, settings.money)
#         result = await session.execute(query)
#         data = result.fetchall()  # Получение всех строк
#         return data