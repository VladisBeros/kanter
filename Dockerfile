# Базовий імідж
FROM python:3.11-slim

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код
COPY . .

# Запуск програми
CMD ["python", "main.py"]