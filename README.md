![foodgram_workflow workflow](https://github.com/kudinov-prog/foodgram-project/workflows/foodgram_workflow%20workflow/badge.svg)

## Сайт "Продуктовый помощник FoodGram"

Ссылка на сайт [CLICK](https://foodbook.tk/ "Продуктовый помощник")

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд, совпадающие ингредиенты блюд суммируются. На страницах со списками рецептов работает фильтрация по тегам (завтрак, обед, ужин). В базу редварительно загружен большой список ингредиентов для рецептов.

#### Инфраструктура
* Проект работает с СУБД PostgreSQL.
* Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn.
* Контейнер с проектом обновляется на Docker Hub.
* В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn.
* Данные сохраняются в volumes.

#### Стек
* Python 3.8, Django 3, PostgreSQL, Gunicorn, Nginx, Docker, Яндекс.Облако(Ubuntu 20.04)

#### Переменные окружения

Для запуска базы данных в корневой папке проекта должен находиться файл 
`.env` с переменными для БД (ниже пример содержимого файла):

```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgresql          # название БД
POSTGRES_USER=postgresql_user   # пользователь БД
POSTGRES_PASSWORD=postgresql    # пароль БД
DB_HOST=db
DB_PORT=5432

```

## Установка проекта
Для установки на локальной машине потребуется:
* Клонировать репозиторий
* Установить и настроить Docker

## Запуск приложения
Для запуска сборки проекта перейти в папку с проектом и выполнить
команду:

```
docker-compose up -d
```

После выполнения сборки запустить миграцию баз данных:

```
docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py migrate
```

Для создания суперпользователя выполнить команду 

```
docker-compose run web python manage.py createsuperuser
```

Проект поставляется с набором первичных данных `fixtures.json`.

Для заполнение БД первичным набором данных выполнить команду

```
docker-compose run web python manage.py loaddata fixtures.json
```

Для запуска сборки статических файлов выполнить команду

```
docker-compose run web python manage.py loaddata collectstatic
```

Для заполнения базы набором ингредиентов, необходимо копировать в нее данные из файла data/ingredients.csv. Сделать это можно выполнив команду в базе postgresql

```
COPY recipes_ingredient(title, unit) FROM '<абсолютный путь до папки>/foodgram-project/ingredients.csv' DELIMITER ',' CSV;
```

Для локального запуска надо исправить в файле `.env` в строке DB_HOST=localhost, а в файле settings.py Debug=True
