from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import SessionLocal
from app.db import crud
from app import schemas

router = APIRouter(prefix="/books", tags=["books"])

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Book])
def read_books(
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if category_id:
        books = crud.get_books_by_category(db, category_id)
    else:
        books = crud.get_books(db, skip=skip, limit=limit)
    return books

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")
    return crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url or ""
    )

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    existing = crud.get_book(db, book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    if book_update.category_id is not None:
        category = crud.get_category(db, book_update.category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")
    updated = crud.update_book(db, book_id, **book_update.dict(exclude_unset=True))
    return updated

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return None