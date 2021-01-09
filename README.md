# foodgram-project
foodgram-project

source food_venv/scripts/activate
django-admin startproject foodgram
python manage.py runserver
python manage.py startapp recipe
python manage.py makemigrations
python manage.py migrate