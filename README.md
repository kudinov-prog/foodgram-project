## Сайт "Продуктовый помощник FoodGram"

Прямая ссылка на сайт --> [CLICK](http://130.193.45.150 "Продуктовый помощник") <--

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Инфраструктура
* Проект работает с СУБД PostgreSQL.
* Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn.
* Контейнер с проектом обновляется на Docker Hub.
* В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn.
* Данные сохраняются в volumes.

#### Стек: Python 3, Django, PostgreSQL, gunicorn, nginx, Яндекс.Облако(Ubuntu 20.04), Docker

## Установка проекта
Для установки на локальной машине потребуется:
* Скачать файлы проекта из репозитория
* Установить и настроить Docker

## Запуск приложения
В корневом каталоге проекта необходимо собрать образ из прилагающихся dockerfile.
Для этого используем команду:
````
sudo docker-compose build
````
После успешного выполнения команды, присутпаем к запуску приложения:
````
sudo docker-compose up
````
Далее необходимо войти в контейнер Web для настройки приложения
Узнаем ID_контейнера web командой:
````
sudo docker container ls -a
````
Заходим в контейнер web:
````
sudo docker exec -ti id_контейнера bash
````

Создадим суперпользователя:
````
python manage.py createsuperuser
````

В данной версии проекта все данные для базы данных postgresql загружаются автоматически при миграции Django.

Приложение запущено и готово к использованию.
