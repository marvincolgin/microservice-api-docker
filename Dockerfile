# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install code
COPY Pipfile Pipfile.lock /code/
COPY ./api/__init__.py /code/api/
copy ./api/factory.py /code/api/
RUN ls -lR /code

# Install dependencies
RUN pip install pipenv
RUN pipenv install --system

# Run It
CMD export FLASK_APP=api ; flask run
