#!/bin/sh
set -e

# Ждём, пока база данных станет доступна (необязательно, но полезно)
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL is up - executing command"

# Выполняем миграции
poetry run python manage.py migrate --noinput

# (Опционально) Собираем статику
# poetry run python manage.py collectstatic --noinput

# Запускаем сервер
echo "Starting server..."
exec poetry run python manage.py runserver 0.0.0.0:8000
