import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "octagon_db")
DB_USER = os.getenv("DB_USER", "octagon")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")

# Строка подключения
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаём движок
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для отладки

# Базовый класс для моделей
Base = declarative_base()

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии (используется в CRUD)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
