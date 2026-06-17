import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()

    print("\n=== КАТЕГОРИИ ===")
    categories = crud.get_categories(db)
    for cat in categories:
        print(f"  {cat.id}: {cat.title}")

    print("\n=== КНИГИ ===")
    books = crud.get_books(db)
    for book in books:
        print(f"  {book.id}: {book.title} (цена: {book.price}) – категория: {book.category.title}")
        if book.description:
            print(f"    Описание: {book.description}")
        if book.url:
            print(f"    Ссылка: {book.url}")

    db.close()

if __name__ == "__main__":
    main()