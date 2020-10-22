release: python manage.py makemigrations && python manage.py migrate
web: gunicorn journal-app.config.wsgi.py --log-file -
