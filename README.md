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

## Running Migrations (create table in database)

> python manage.py migrate

## check migration code that sent to the database

> python manage.py sqlmigrate ["app_name"] ["sequence_number"]
>
> For example python manage.py sqlmigrate store 002

## Revert migrations

> python manage.py migrate ["app_name"] ["previous_sequence_number"]

## connect to mysql

> pipenv install mysqlclient

## create and run custom sql through empty migration

> python manage.py makemigrations ["Folder_name"] --empty
>
> operations = [

        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')
        """, """
            DELETE FROM store_collection
            WHERE title='collection1'
        """)
    ]

>

## websites

> https://mockaroo.com/
>
> https://docs.djangoproject.com/en/4.2/ref/models/querysets/#values
>
> https://docs.djangoproject.com/en/4.2/ref/models/database-functions/
>
> https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#modeladmin-options
>
> https://www.django-rest-framework.org/

## Create New User

> python manage.py createsuperuser

## to handle restful api's

> pipenv install djangorestframework
