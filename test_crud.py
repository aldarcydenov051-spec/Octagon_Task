from app.db.db import SessionLocal
from app.db import crud

db = SessionLocal()

# Создаём категорию
cat = crud.create_category(db, "Фантастика")
print(f"Создана категория: {cat.title} (id={cat.id})")

# Создаём книгу
book = crud.create_book(db, "Дюна", "Научно-фантастический роман", 1200.0, cat.id)
print(f"Создана книга: {book.title} (id={book.id})")

# Читаем книги
books = crud.get_books(db)
for b in books:
    print(f"Книга: {b.title}, цена {b.price}, категория {b.category.title}")

db.close()