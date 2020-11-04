release: python manage.py makemigrations && python manage.py migrate --fake journal zero && python manage.py migrate --fake journal_mail zero && python manage.py migrate --fake users zero
web: gunicorn config.wsgi --log-file -
