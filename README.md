# Octagon_Task
REST API для управления книгами и категориями на базе FastAPI + PostgreSQL.
## Стек
- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL (через WSL)
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/aldarcydenov051-spec/Octagon_Task.git
   cd Octagon_Task
2. Создайте виртуальное окружение и активируйте его:
python3 -m venv venv
source venv/bin/activate
3. Установите зависимости:
pip install -r requirements.txt
4. Настройте переменные окружения в файле .env (пример):
DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345
5. Запустите сервер:
uvicorn app.mainFastAPI:app --reload --host 0.0.0.0 --port 8000
6. http://localhost:8000/docs