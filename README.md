# sidus-task

_Тестовое задание для бэкенд-разработчика Sidus Heroes._

```
Треубется написать простой апи при помощи FastAPI, подключенный к Postgresql БД.
Условия:
1) В базе данных должна быть таблица user с произвольными столбцами;
2) Описание и работа с БД при помощи SQLalchemy;
3) В апи должно быть три эндпоинта - get_user, сreate_user, update_user;
4) Изменять поля юзера может только он сам (нужна авторизация);
5) Результат get_user должен кешироваться;
6) При измении полей юзера кеш должен сбрасываться (во всех воркерах);
7) Докерфайл или иной способ развернуть проект и проверить работу апи;
8) Покрытие тестами;
9) Asyncio;
10) PEP-8.
Приветствуются любые дополнительные фичи с применением знакомых технологий на свой вкус.
Это могут быть, например, другие связанные таблицы БД cо сложными запросами к ним,
публикация сообщений о регистрации юзера в брокер сообщений,
выполнение отложенных задач при помощи Сelery и т.д.
```

<img src="demo-sidus-api.png">

### Запуск

1. Запустить БД: 
```
docker run --name sidus_db -d -e POSTGRESQL_PASSWORD=userPass123 -e POSTGRESQL_USERNAME=admin_user -e POSTGRESQL_DATABASE=sidus_db -p 5437:5432 bitnami/postgresql:13
```
3. `docker-compose up`
4. http://0.0.0.0:8000/docs

### Замечания

В описании тестового задания приветствовалось использование технологий на свой вкус, поэтому для описания моделей взял https://github.com/tiangolo/sqlmodel, это обёртка над Алхимией от создателя FastAPI, которая позволяет писать более лаконичный код + завёз Celery с отправкой email'а. 

Postgresql запускается заранее, чтобы не нужно было писать sh-скрипт, который будет ожидать запуска PostgreSQL, плюс по-хорошему .env не должен лежать в репо и вообще нужно использовать отдельное хранилище для креденшлов, и пароли должны быть сложными. Но для тестового мне так сподручнее было. 

В п.3 позволил себе не называть эндпоинты - get_user, сreate_user, update_user, потому что это плохая практика при создании REST, соответственно сделал `/users` и в зависимости от метода получаем нужный результат, изменение пользователей через `/admin`. Ещё добавил версионирование API, плюс `healthcheck`, плюс `users/me`, плюс удаление через `is_deleted`, потому что это всё тоже best practices. Если нужно сделать В ТОЧНОСТИ как в описании тестового, то сообщите до начала технического собеседования, я сделаю PR.
