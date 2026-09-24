import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemed_project.settings')

# Setup Django
import django
django.setup()

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()