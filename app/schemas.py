from pydantic import BaseModel
from typing import Optional

# ---------- Схемы для категорий ----------
class CategoryBase(BaseModel):
    title: str

# Схема для создания (POST) и обновления (PUT) – используем ту же основу
class CategoryCreate(CategoryBase):
    pass

# Схема для ответа (GET) – добавляем id
class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True   # вместо orm_mode


# ---------- Схемы для книг ----------
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: int

# Схема для создания (POST) – полностью повторяет BookBase
class BookCreate(BookBase):
    pass

# Схема для обновления (PUT / PATCH) – все поля опциональны
class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    category_id: Optional[int] = None

# Схема для ответа (GET) – добавляем id и вложенную категорию
class Book(BookBase):
    id: int
    category: Category   # вложенный объект категории

    class Config:
        from_attributes = True