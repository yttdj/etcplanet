import django.core.wsgi
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = django.core.wsgi.get_wsgi_application()
