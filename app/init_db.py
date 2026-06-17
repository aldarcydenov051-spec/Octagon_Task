import sys
import os

# Добавляем корень проекта в sys.path, чтобы импорты работали
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, engine
from app.db import models, crud

def init_db():
    # 1. Создаём таблицы, если их нет
    models.Base.metadata.create_all(bind=engine)
    print("Таблицы созданы (или уже существуют).")

    # 2. Открываем сессию
    db = SessionLocal()

    # 3. Проверяем, есть ли уже категории
    if crud.get_categories(db):
        print("База уже содержит данные. Пропускаем вставку.")
        db.close()
        return

    # 4. Добавляем категории
    categories_data = ["Фантастика", "Детектив", "Научная литература", "Роман"]
    category_objects = []
    for cat_title in categories_data:
        cat = crud.create_category(db, cat_title)
        category_objects.append(cat)
        print(f"Добавлена категория: {cat_title}")

    # 5. Добавляем книги для каждой категории
    books_data = {
        "Фантастика": [
            {"title": "Дюна", "description": "Научно-фантастический роман Фрэнка Герберта", "price": 1200.0},
            {"title": "1984", "description": "Антиутопия Джорджа Оруэлла", "price": 950.0},
            {"title": "Автостопом по галактике", "description": "Юмористическая фантастика Дугласа Адамса", "price": 850.0}
        ],
        "Детектив": [
            {"title": "Собака Баскервилей", "description": "Повесть о Шерлоке Холмсе", "price": 700.0},
            {"title": "Убийство в Восточном экспрессе", "description": "Детектив Агаты Кристи", "price": 800.0}
        ],
        "Научная литература": [
            {"title": "Краткая история времени", "description": "Стивен Хокинг о космологии", "price": 1100.0},
            {"title": "Структура научных революций", "description": "Томас Кун", "price": 900.0},
            {"title": "Эгоистичный ген", "description": "Ричард Докинз", "price": 1000.0}
        ],
        "Роман": [
            {"title": "Мастер и Маргарита", "description": "Михаил Булгаков", "price": 750.0},
            {"title": "Война и мир", "description": "Лев Толстой", "price": 1300.0}
        ]
    }

    for cat_title, books in books_data.items():
        # находим объект категории по названию
        category = crud.get_category_by_title(db, cat_title)
        if not category:
            print(f"Категория '{cat_title}' не найдена, пропускаем.")
            continue
        for book_info in books:
            crud.create_book(
                db,
                title=book_info["title"],
                description=book_info["description"],
                price=book_info["price"],
                category_id=category.id,
                url=""  # пока оставляем пустым
            )
            print(f"  Добавлена книга: {book_info['title']}")

    db.close()
    print("Инициализация завершена.")

if __name__ == "__main__":
    init_db()