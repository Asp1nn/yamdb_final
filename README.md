# api_yamdb
api_yamdb - сервис отзывов о различных произведениях (фильмы, музыка и т.п.)
Для того, чтобы запустить проект необходимо установить и настроить Docker, как это сделать описано по ссылке: <br>https://timeweb.com/ru/community/articles/ustanovka-i-nastroyka-docker-1
Далее клонируйте репозиторий командной: git clone <адрес репозитория>
Необходимо создать файл .env в директории где находится setting.py и заполнить его данными:
    <br>
    <br>SECRET_KEY='p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'
    <br>EMAIL_HOST_USER='yamdbproject@gmail.com'
    <br>EMAIL_HOST_PASSWORD='asd-1234'
    <br>DB_NAME=postgres
    <br>POSTGRES_USER=postgres
    <br>POSTGRES_PASSWORD=postgres
    <br>DB_HOST=db
    <br>DB_PORT=5432
    <br> 
После клонирования репозитория с githab и создания файла .env:
    <br>1. Собрать образ docker-compose up --build
    <br>2. Применить миграции docker-compose exec web python manage.py migrate --noinput
    <br>3. Применить docker-compose exec web python manage.py collectstatic --no-input
    <br>4. Создать суперюзера docker-compose exec web python manage.py createsuperuser
    <br>5. Заполнить первоночальными данными:
    <br>docker-compose exec web python3 manage.py shell  
    Выполнить в открывшемся терминале:
    <br>>>> from django.contrib.contenttypes.models import ContentType
    <br>>>> ContentType.objects.all().delete()
    <br>>>> quit()
    <br>docker-compose exec web python manage.py loaddata fixtures.json
    <br>
    <br>Используемые технологии:
    <br>Python 3.9
    <br>Django 2.2.6
    <br>Gunicorn 20.1.0
    <br>Nginx 1.19.3
    <br>Docker
    <br>Docker 20.10.8
    <br>
    <br> Автор проекта:
    <br> Asp1n
    <br>
    <br> ![workflow](https://github.com/asp1n/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
