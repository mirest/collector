release: python manage.py migrate; python manage.py loaddata fixtures/*
web: gunicorn config.wsgi 