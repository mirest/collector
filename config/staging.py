from .default import *  # noqa
import django_heroku


django_heroku.settings(locals(), test_runner=False)

ALLOWED_HOSTS += ['.herokuapp.com']  # noqa
