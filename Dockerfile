
FROM python:3.7

COPY . .

ENV PYTHONUNBUFFERED 1
RUN pip install pipenv &&\
    pipenv install --python 3.7 --skip-lock&&\
    pipenv shell&&\
    pipenv install --skip-lock
CMD ["gunicorn","config.wsgi:application","--workers 3"]