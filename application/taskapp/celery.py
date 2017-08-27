#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/4/17
# email: me@jarrekk.com
from __future__ import absolute_import

import os
import traceback
from functools import wraps

from celery import Celery, shared_task
from django.conf import settings
from django.core.mail import mail_admins

# set Django settings module for celery program.
config = '.'.join(['settings', os.environ.get('ENV', 'development')])
os.environ['DJANGO_SETTINGS_MODULE'] = config

app = Celery(os.environ.get('PROJECT_NAME'))
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto discover tasks on installed apps & project root folder
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + [os.environ.get('PROJECT_NAME') + '.tasks'])


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def shared_task_email(func):
    """
    Replacement for @shared_task decorator that emails admins if an exception is raised.
    """
    @wraps(func)
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            subject = "Celery task failure"
            message = traceback.format_exc()
            mail_admins(subject, message)
            raise
    return shared_task(new_func)
