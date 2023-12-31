create the virtual environment
    python3 -m venv projenv 

activate the virtual environment
    cd ..
    source projenv/bin/activate
    cd log_project

install the requirements
    pip install -r requirement.txt

create Django project 
    Django-admin startapp

install Django
	python3 -m pip install django

Create project
	django-admin startproject log_project

Run
	python3 manage.py runserver

create an app
    python manage.py startapp log_management

Create and Apply Migrations
    python manage.py makemigrations
    python manage.py migrate

Install Elasticsearch DSL
    pip install django-elasticsearch-dsl

activate elasticsearch 
    cd downloads
    cd elasticsearch-8.11.1  
    ./bin/elasticsearch


install postgresql
    pip install django psycopg2

start db
    brew services start postgresql

stop db
    brew services stop postgresql
    
