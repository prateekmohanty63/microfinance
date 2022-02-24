# Django Microfinance

## About this project

Microfinance is an open source and free platform for collecting KYC data, structuring loans, and setting up other financial products such as insurance or asset financing. The platform is focused on the unique lending environment of emerging economies. 


## How to run the project and get started

You can get started by going through the typical Django initiation steps noted below:

- Make sure you are in a virtualenv (it is usually recommended to set up a new one specifically for this project)
- Install everything from requirements.txt using ```pip install -r requirements.txt``` (use `pip3` if running two version of python - this project is running on python3)
- Make sure you create a local database in ```core.settings.base.py```. We always use a format of ```[project name]-local```, so in this case it's ```microfinance-local```:
```
local_database = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'microfinance-local',
          'USER': 'YOUR LOCAL USER',
          'PASSWORD': 'YOUR LOCAL PASSWORD',
          'HOST': 'localhost',
          'PORT': '5432',
      }
}
```
- Run ```python3 manage.py makemigrations``` to create database migrations
- Run ```python3 manage.py migrate``` to create database tables / initial setup
- Run ```python3 manage.py createsuperuser``` to create an admin user
- Run ```python3 manage.py runserver``` for start the local server
- The project should be running now at http://127.0.0.1:8000/
- The admin panel should be running now at http://127.0.0.1:8000/admin

Please note that the project does rely on some third party services, such as Mailgun for things like password reset (in production) or S3 for file storage (in both dev and production).

## Celery and Background Tasks

The project relies on celery for background tasks, such as sending out emails. To run celery, make sure you have redis running locally then start celery. You will need to be within the same virtualenv of the project.

In one terminal run ```redis-server``` (doesn't need to be in the virtualenv)
In another terminal in the virtualenv run ```celery -A core worker -l info``` to start the background worker
You can also run ```celery -A core beat -l info``` in another terminal within the virtualenv for more info


## Deployment

The project is setup to deploy to Heroku

- There is a setup for dev and production, using an environment variable `environment` on Heroku to designate 'production' settings.
- The `main` branch is always the most up to date code.

