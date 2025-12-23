FROM python:3.11-slim

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY tg_bot.py menu_text.py ./

# Создаем директорию для логов
RUN mkdir -p /app/data

# Запускаем бота
CMD ["python", "tg_bot.py"]

