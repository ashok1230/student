#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer

from django.core.management import setup_environ    
import settings
setup_environ(settings)

from django.core.handlers.wsgi import WSGIHandler as DjangoWSGIApp
application = DjangoWSGIApp()
server = WSGIServer(("192.168.0.50", 9000), application)
print "Starting Green server on http://192.168.0.50:9000"
server.serve_forever()
back
#!/usr/bin/env python
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
    
    
routers

"""
NewWebsite.com's router
Establishes rules to forward user and session db requests 
to ExampleA.com unless we are accessing the admin.
"""
import threading

# Object to hold request data
request_cfg = threading.local()

class RouterMiddleware(object):
    """
    Sets a flag if we are accessing Django admin to 
    prevent database rerouting for the auth model.  
    Removes the flag once the request has been processed.
    """

    def process_view(self, request, view_func, args, kwargs):
        if request.path.startswith('/admin'):
            request_cfg.admin = True

    def process_response(self, request, response):
        if hasattr(request_cfg, 'admin'):
            del request_cfg.admin
    return response

class UserSessionRouter(object):
    """
    Redirects database IO for the auth and sessions 
    models to OldWebsite.com.
    """

    def db_for_read(self, model, **hints):
        if not hasattr(request_cfg, 'admin'):
            if model._meta.app_label == 'auth':
                return 'usersandsessions'
            elif model._meta.app_label == 'accounts':
                return 'usersandsessions'
            elif model._meta.app_label == 'sessions':
                return 'usersandsessions'
        return None

    def db_for_write(self, model, **hints):
        if not hasattr(request_cfg, 'admin'):
            if model._meta.app_label == 'auth':
                return 'usersandsessions'
            elif model._meta.app_label == 'accounts':
                return 'usersandsessions'
            elif model._meta.app_label == 'sessions':
                return 'usersandsessions'
        return None
