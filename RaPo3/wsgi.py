"""
WSGI config for RaPo3 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
# import uwsgi

# from core.task import wy_request

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RaPo3.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# uwsgi.register_signal(82, "", wy_request)
# uwsgi.add_cron(82, 0, 20, -1, -1, -1)
