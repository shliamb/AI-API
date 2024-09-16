
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
# from keys import USER_DB, PASWORD_DB


import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
USER_DB, PASWORD_DB = os.environ.get('USER_DB'),  os.environ.get('PASWOR_DB')

                                                            # @localhost  # @postgres
DATABASE_URL = f"postgresql+asyncpg://{USER_DB}:{PASWORD_DB}@postgres:5432/my_database"
engine = create_async_engine(DATABASE_URL) # Создание асинхронного движка для работы с базой данных
Base = declarative_base() # Создание базового класса для объявления моделей
Column = sqlalchemy.Column



# Users Main Data
class UsersBase(Base):  # username - точка всего
    __tablename__ = 'users'
    # User data
    username = Column(sqlalchemy.String(50), primary_key=True, nullable=False, unique=True, index=True) # Username пользователя, для идентификации в API, уникальное.
    appkey = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, index=True) # Автоматически создается UUID в качестве API Key - 9a5bce5f-4462-4d12-a66c-d5958b19ee8
    is_failed = Column(sqlalchemy.Integer(), nullable=False, default=0, server_default="0", index=True) # Неудачные попытки доступа
    is_block = Column(sqlalchemy.Boolean, default=False, server_default="False", nullable=False, index=True) # Заблокирован ли пользователь из-за колл. не верных вводов.
    date_block = Column(sqlalchemy.DateTime, nullable=True) # Дата и время блокировки, для отсчета времени блокировки
    date_last_activ = Column(sqlalchemy.DateTime, nullable=True) # Дата последней активности
    money = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # Денег на счете в $, пезволит унифицироваться и выстроить путь "идеального" приложения
    money_currency = Column(sqlalchemy.String(10), default="USD", server_default="USD", nullable=False) # Сразу все в $, так проще, раньше все проги так и работали, возвращаемся))
    # Telegram
    id = Column(sqlalchemy.BigInteger, unique=True, nullable=False, index=True) # Telegram id
    name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    full_name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    first_name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    last_name = Column(sqlalchemy.String(50), nullable=True) # Telegram
    ###
    stat = relationship("Statistics")
    ###

# User spending statistics - One-to-many
class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(sqlalchemy.Integer, primary_key=True)
    time = Column(sqlalchemy.DateTime, nullable=True) 
    use_model = Column(sqlalchemy.String(100), nullable=False) # Использованная модель
    sesion_token = Column(sqlalchemy.BigInteger, default=0, server_default="0",  nullable=False) # Использованно токенов
    price_1_tok = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) # Цена токена, если менялась, то будет видно
    total_price = Column(sqlalchemy.Float, default=0, server_default="0", nullable=False) #  Вся цена
    ###
    username_table_stat = Column(sqlalchemy.String(50), ForeignKey("users.username"), index=True) # username user telegram
    ###


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