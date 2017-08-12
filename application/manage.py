#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/3/17
# email: me@jarrekk.com
import os
import sys

if __name__ == "__main__":
    config = '.'.join(['settings', os.environ.get('ENV', 'development')])
    os.environ['DJANGO_SETTINGS_MODULE'] = config
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)

    package = '.'.join([os.environ.get('PROJECT_NAME', 'project_name'), 'load'])
    name = 'load_after_app_start'

    load_after_app_start = getattr(__import__(package, fromlist=[name]), name)

    load_after_app_start()
