release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn journal-app.config.wsgi.py --log-file -
