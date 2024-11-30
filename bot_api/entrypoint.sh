#!/bin/sh

# Применить и создать миграции
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Собрать статические файлы
python manage.py collectstatic --noinput
cp -r ./staticfiles/ /var/html/

# Создать суперпользователя
python manage.py create_superuser

# Запуск Gunicorn
gunicorn --bind 0.0.0.0:8000 core.wsgi:application
