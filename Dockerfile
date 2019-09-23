# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install code (Only for docker, docker-compose uses .yml specs)
COPY ./api/__init__.py /code/api/
COPY ./api/factory.py /code/api/

# Install dependencies
COPY ./Pipfile ./Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system

# Run It
CMD export FLASK_APP=api ; flask run --host 0.0.0.0 --port 5000
