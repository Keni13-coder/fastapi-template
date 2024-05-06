# FastApi Template
[![Python Code and Alembic Checks](https://github.com/Keni13-coder/fastapi-template/actions/workflows/ci.yml/badge.svg?branch=develop&event=pull_request)](https://github.com/Keni13-coder/fastapi-template/actions/workflows/ci.yml)
### Запуск шаблона:
#### Docker-compose
1) Создайте файл .env, данные нужные для запуска можно посмотреть в .env.example
2) Примените команду для запуска: ```docker-compose up -d --build```
3) Перейдите в контейнер с ботом, для этого после полного запуска введите следующую команду: ```docker exec -it <название_контейнера> bash```
4) Примените миграции: ```alembic upgrade head```

Документация к API доступна по url: http://localhost:8000/docs/

#### Uvicorn
1) Создайте файл .env, данные нужные для запуска можно посмотреть в .env.example
    * Основаная директория проекта app.app, там же нужно создать env, далее оталкивайтесь от этого.
2) Выполните команду создание виртуального окружения ```poetry install --no-root```
    * Перейдите в виртуального окружения ```poetry shell```
3) Примените миграции: ```alembic upgrade head```
    * Прежде чем выполнить миграцию, проверте существование базы данных
4) Запустите проект командой ```uvicorn app.main:app```

Документация к API доступна по url: http://localhost:8000/docs/

#### Дополнительно

Стоит принимать во внимание, что у вас не получится ознакомиться с функциональной частью в docs, так как взаимодействия с некоторыми поинтами видётся через заголовки и печеньки.
