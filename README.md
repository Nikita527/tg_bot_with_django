# Тестовый сайт на Django с авторизацией через Telegram

## Технологии:
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Aiogram](https://aiogram.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

## Как запустить:
1. Клонируйте репозиторий
2. Скачайте или установите Docker
3. Перейдите по пути к файлу docker-compose.dev.yaml
    - cd infra/dev
3. В файл docker-compose.dev.yaml вставьте токен вашего бота и имя вашего бота
    - (получить можно в [BotFather](https://t.me/BotFather))
4. Запустите Docker-команду "docker-compose -f docker-compose.dev.yaml up -d"
5. Проект будет доступен по адресу http://localhost

## Как остановить:
1. Выполнить команду "docker-compose -f docker-compose.dev.yaml down"
