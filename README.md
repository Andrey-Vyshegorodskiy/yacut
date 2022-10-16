# YaCut
Сервис укорачивания ссылок с web интерфейсом и REST API. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Ключевые возможности сервиса
- Генерация коротких ссылок и связь их с исходными длинными ссылками
- Переадресация на исходный адрес при обращении к коротким ссылкам
- /api/id/ — POST-запрос на создание новой короткой ссылки;
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.


Доступны web и api интерфейсы.

## Технологии
- Python 3.10
- Flask 2.0
- Jinja2 3.0
- SQLAlchemy 1.4

## Использование
Клонировать репозиторий и перейти в него в командной строке:

```commandline
git clone 
```

```commandline
cd yacut
```

Cоздать и активировать виртуальное окружение:

```commandline
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```commandline
    source venv/bin/activate
    ```

* Если у вас Windows

    ```commandline
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```commandline
python3 -m pip install --upgrade pip
```

```commandline
pip install -r requirements.txt
```

Выполнить миграции:

```commandline
flask db upgrade
```


Запуск проекта:
```commandline
flask run
```

## Автор
Андрей Вышегородский
https://github.com/Andrey-Vyshegorodskiy