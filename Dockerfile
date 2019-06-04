FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install pipenv
RUN pipenv install
COPY . .