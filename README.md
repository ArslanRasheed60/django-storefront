### to run virtual environment

> pipenv shell

<!-- ### to run a command inside virtual environment

> pipenv run -->

### to start a project

> django-admin startproject storefront .

### to run server

> python manage.py runserver

## Create a new app

> python manage.py startapp playground
>
> - playground is the name of the **new app**
> - we need to register it to the **settings.py file**

## Create migrations

> python manage.py makemigrations

## Running Migrations

> python manage.py migrate

## check migration code that sent to the database

> python manage.py sqlmigrate ["app_name"] ["sequence_number"]
>
> For example python manage.py sqlmigrate store 002
