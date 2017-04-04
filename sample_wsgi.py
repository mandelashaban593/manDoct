import os
import sys

path = '/home/pythonanywhereusername/projectname'  # use your own pythonAny username here

if path not in sys.path:
	sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'projectname.settings'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
applicaton = StaticFilesHandler(get_wsgi_application())
