
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
import sqlalchemy
from typing import AsyncGenerator
# from keys import user_db, paswor_db


import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
user_db, paswor_db = os.environ.get('USER_DB'),  os.environ.get('PASWOR_DB')

                                                            # @localhost  # @postgres
DATABASE_URL = f"postgresql+asyncpg://{user_db}:{paswor_db}@localhost:5432/my_database"
engine = create_async_engine(DATABASE_URL) # Создание асинхронного движка для работы с базой данных
Base = declarative_base() # Создание базового класса для объявления моделей
Column = sqlalchemy.Column



# Users Main Data
class UsersBase(Base):
    __tablename__ = 'users'
    # Telegram
    id = Column(sqlalchemy.BigInteger, primary_key=True, unique=True, nullable=False, index=True) # Telegram id
    name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    full_name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    first_name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    last_name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    # User data
    username = Column(sqlalchemy.String(50), nullable=False, unique=True, index=True) # Username пользователя, для идентификации в API, уникальное.
    appkey = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, index=True) # Автоматически создается UUID в качестве API Key - 9a5bce5f-4462-4d12-a66c-d5958b19ee8
    is_failed = Column(sqlalchemy.Integer(), nullable=False, default=0, server_default="0", index=True) # Неудачные попытки доступа
    is_block = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False, index=True) # Заблокирован ли пользователь из-за колл. не верных вводов.
    date_block = Column(sqlalchemy.DateTime, nullable=True) # Дата и время блокировки, для отсчета времени блокировки
    date_last_activ = Column(sqlalchemy.DateTime, nullable=True) # Дата последней активности
    money = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # Денег на счете в $, пезволит унифицироваться и выстроить путь "идеального" приложения
    money_currency = Column(sqlalchemy.String(10), default="USD", server_default="USD", nullable=False) # Сразу все в $, так проще, раньше все проги так и работали, возвращаемся))
    ###
    stat = relationship("Statistics")
    ###

# User spending statistics - One-to-many
class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(sqlalchemy.Integer, primary_key=True)
    time = Column(sqlalchemy.DateTime, nullable=True) 
    use_model = Column(sqlalchemy.String(50), nullable=False) # Использованная модель
    sesion_token = Column(sqlalchemy.Integer, default=0, server_default="0",  nullable=False) # Использованно токенов
    price_1_tok = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # Цена токена, если менялась, то будет видно
    price_sesion_tok = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) #  Вся цена
    ###
    users_telegram_id = Column(sqlalchemy.BigInteger, ForeignKey("users.id"), index=True) # id user telegram
    ###


# Exchange Data - будут строки с валютами и их курс по отношению к $, пока что только RUB, но можно будет и другие, посмотрим. Курс будет нужен для ввода старонней валюты, отличной от $, но внутренняя валюта будет только $
class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(sqlalchemy.Integer, primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True) # Дата обновления курса
    rate = Column(sqlalchemy.Float(), nullable=True) # Курс валюты к $
    currency = Column(sqlalchemy.String(10), nullable=True) # Внутренее обозначение или название валюты, например RUB
    counter = Column(sqlalchemy.BigInteger, nullable=True) # Возможно я захочу собирать статистику обмена
    ###

class Backup(Base):
    __tablename__ = 'backup'
    id = Column(sqlalchemy.Integer, primary_key=True)
    date = Column(sqlalchemy.DateTime, nullable=True)
    date_changes = Column(sqlalchemy.DateTime, nullable=True)
    task = Column(sqlalchemy.String(1000), nullable=True)
    is_complite = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False) 
    ####
####





# Build Table to DB
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Creature session interactions to DB
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session