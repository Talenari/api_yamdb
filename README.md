# Проект «YaMDb».

## Описание
API для сервиса YaMDb.
YaMDb собирает отзывы пользователей на различные фильмы, книги и музыку. 

### Стек технологий
- Python 3.9
- Django 2.2.16
- Django REST framework 3.12.4
- djangorestframework-simplejwt 5.0.0
- python-dotenv 0.19.2

## Документация

После запуска проекта документация доступна по адресу http://127.0.0.1:8000/redoc/

## Запуск проекта в dev-режиме

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Talenari/api_yamdb
```

```
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```
Создать суперпользователя:

```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов
```
Получить список всех произведений. Права доступа: Доступно без токена.
http://127.0.0.1:8000/api/v1/titles/
```
```
Получить список всех отзывов. Права доступа: Доступно без токена.
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```
Получить список всех комментариев к отзыву по id Права доступа: Доступно без токена.
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```


## Запуск тестов

Из корня проекта:

```
pytest
```

### Разработчики

```
https://github.com/KhahaDu - Дмитрий Хайдуков
Пользователи и аутентификация
```

```
https://github.com/Talenari - Alena ♥ Tale
Произведения и категории
```

```
https://github.com/Denriandro - Евгений Галеев
Отзывы и комментарии
```
