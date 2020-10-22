release: python manage.py makemigrations && python manage.py migrate
web: gunicorn config.wsgi.py --log-file -
