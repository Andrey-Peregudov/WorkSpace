# Образ Python версии 3.12
FROM python:3.12
# Рабочая директория
WORKDIR /app
# Копируем зависимости
COPY app/requirements.txt .
# Устанавливаем зависимости
RUN pip install -r requirements.txt
# Устанавливаем переменное окружение
ENV FASTAPI "/app/main.py"
# Копируем все файлы
COPY . .
# Запускаем приложение с помощью Uvicorn
CMD ["python", "-m" , "fastapi", "run", "--host=0.0.0.0", "--port=8080"]