# Базовый образ Python
FROM python:3

# Рабочая директория в контейнере
WORKDIR /code

# Копируем зависимости в контейнер
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . .