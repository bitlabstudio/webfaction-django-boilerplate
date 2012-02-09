import os, sys, site

site.addsitedir('/home/ENV_USER/Envs/VENV_NAME/lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

activate_this = os.path.expanduser("~/Envs/VENV_NAME/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))
project = '/home/ENV_USER/webapps/DJANGO_APP_NAME/project/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
