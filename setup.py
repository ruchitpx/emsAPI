python -m venv venv
venv\scripts\activate

pip install django djangorestframework djangorestframework-simplejwt django-filter pillow celery redis pytest pytest-django
python -m pip install --upgrade pip

pip freeze > requirements.txt
pip install -r requirements.txt

django-admin startproject emsAPI .
python manage.py startapp events
python manage.py startapp users

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
admin
admin@gmail.com
admin
admin
y

python manage.py createsuperuser
tom
tom@gmail.com
tom@1234
tom@1234

python manage.py createsuperuser
jerry
jerry@gmail.com
jerry@1234
jerry@1234

python manage.py runserver