# Dockerfile

# Python version
FROM python:3.8

WORKDIR /journal-app

# Allows docker to cache installed dependencies between builds
COPY requirements/base.txt requirements/base.txt
COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .

EXPOSE 8000

# runs the production server
CMD ["pyton", "journal-app/manage.py", "runserver", "0.0.0.0:8000"]
