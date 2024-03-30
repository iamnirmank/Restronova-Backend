# Project Setup and Documentation

Welcome to the project! Below is a step-by-step guide to help you set up your Django environment, manage migrations, generate API documentation, install dependencies, and schedule background tasks.

## Create and Activate Virtual Environment

```
python -m venv venv
```

## Activate virtual environment
```
venv\Scripts\activate
Migrations and Database Setup
```

## Create and apply migrations
```
python manage.py makemigrations
python manage.py migrate
```

## Generate API documentation using drf-yasg
```
python manage.py generateschema --file openapi-schema.yml
```
## Run the Project
```
python manage.py runserver
```
## Generate requirements.txt
```
pip freeze > requirements.txt
```

## Install dependencies from requirements.txt
```
pip install -r requirements.txt
```

## Collect static files
```
python manage.py collectstatic
```

## Scheduling Background Tasks
Learn How to schedule and execute background tasks in a Django application: _https://www.linkedin.com/pulse/how-schedule-execute-background-tasks-django-aimen-dahmani-frize/_
