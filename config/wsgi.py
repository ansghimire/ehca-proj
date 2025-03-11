import os
import sys
from django.core.wsgi import get_wsgi_application
from decouple import config


# its required if u want to placed all installed applications inside apps/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../apps')))


# Set the default settings module using an environment variable,
# defaulting to development settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE', default='config.settings.development'))

application = get_wsgi_application()
