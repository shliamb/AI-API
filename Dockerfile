FROM python:3.12-slim

# ENV PYTHONUNBUFFERED=1

# Установка apt-utils
RUN apt-get update && apt-get install -y apt-utils

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Указываем команду для запуска приложения при старте контейнера
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80"]
# CMD ["python", "app/run_bot.py"]