# Use the official Python 3.12 slim image as the base image
FROM python:3.12-slim

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    libpq-dev \
    build-essential \
    netcat-openbsd \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*


# Обновляем pip, setuptools, wheel с указанием trusted-host
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org

# Устанавливаем Poetry (без фиксации версии)
RUN pip install --no-cache-dir poetry \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --default-timeout=100

WORKDIR /app

# Копируем файлы с зависимостями
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости (без dev)
RUN poetry install --no-root

# Копируем код проекта (включая entrypoint.sh)
COPY . /app/

# Делаем entrypoint.sh исполняемым
RUN chmod +x /app/entrypoint.sh

# Открываем порт 8000 для нашего Django-приложения
EXPOSE 8000

# Устанавливаем точку входа
ENTRYPOINT ["/app/entrypoint.sh"]
