from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.db import SessionLocal
from app.db import crud
from app import schemas

router = APIRouter(prefix="/categories", tags=["categories"])

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = crud.get_category_by_title(db, category.title)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(db, category.title)

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    updated = crud.update_category(db, category_id, category.title)
    if updated is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_category(db, category_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return None