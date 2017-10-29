#Instal dependencies

```
pip install -r requirements.txt

```

#Запуск

При первичном запуске произвести миграции

```
./manage.py migrate
```

При первичном запуске заполнить модель начальными данными

```
./manage.py loaddata fixtures.json
```

При первичном запуске следует создать суперпользователя

```
./manage.py createsuperuser
```

Сам запуск

```
./manage.py runserver
```

#Тестирование

```
./manage.py test apps.bulletin.tests.test
```
