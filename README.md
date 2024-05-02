# FastApi Template
[![tests-check Status](https://github.com/Keni13-coder/fastapi-template/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/Keni13-coder/fastapi-template/actions/workflows/ci.yml)
### Запуск шаблона:

1) Создайте файл .env, данные нужные для запуска можно посмотреть в .env.example
2) Примените команду для запуска: ```docker-compose up -d --build```
3) Перейдите в контейнер с ботом, для этого после полного запуска введите следующую команду: ```docker exec -it <название_контейнера> bash```
4) Примените миграции: ```alembic upgrade head```

Документация к API доступна по url: http://localhost:80/docs/
