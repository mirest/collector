
FROM python:3.7

COPY . .

ENV PYTHONUNBUFFERED 1
RUN pip install -r requirements.txt
CMD ["gunicorn","config.wsgi:application","--workers 3"]