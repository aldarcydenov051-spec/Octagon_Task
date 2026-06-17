from app.db.db import engine
from app.db import models

def init_db():
    # Создаёт все таблицы, определённые в models
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Таблицы созданы успешно!")