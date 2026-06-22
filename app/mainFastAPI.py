from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text   # <-- импорт text

from app.api import categories, books
from app.db import models
from app.db.db import engine, get_db

# Создание таблиц при старте
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ База данных доступна, таблицы созданы (или уже существуют).")
except Exception as e:
    print(f"❌ Ошибка подключения к БД: {e}")

app = FastAPI(title="Book API", description="API для управления книгами и категориями")

app.include_router(categories.router)
app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в Book API! Используйте /docs для документации."}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "detail": str(e)}