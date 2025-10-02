FROM python:3.12-alpine

WORKDIR /home/ai

# Устанавливаем зависимости
COPY ./ai_requirements.txt .
RUN pip install --no-cache-dir -r ai_requirements.txt

# Копируем код приложения
COPY . .

# Запускаем FastAPI сервер
CMD ["uvicorn", "ai.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
