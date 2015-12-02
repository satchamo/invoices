#!/usr/bin/env python
import sys

import django
from django.conf import settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    ROOT_URLCONF='urls',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'invoices',
    ),
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'cloak.middleware.CloakMiddleware',
    ],
    SECRET_KEY="123",
    INVOICE_APP_NAME="foo",
)

from django.test.utils import get_runner

django.setup()


TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1)

failures = test_runner.run_tests(['invoices'])
sys.exit(bool(failures))
