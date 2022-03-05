#!/home/ec2-user/project_1/venv/bin/python3
"""
WSGI config for project_1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ec2-user/project_1/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')

application = get_wsgi_application()
