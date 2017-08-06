#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/4/17
# email: me@jarrekk.com
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set Django settings module for celery program.
config = '.'.join(['settings', os.environ.get('ENV', 'development')])
os.environ['DJANGO_SETTINGS_MODULE'] = config

app = Celery(os.environ.get('PROJECT_NAME'))
app.config_from_object('django.conf:settings')

# auto discover tasks on installed apps & project root folder
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + [os.environ.get('PROJECT_NAME') + '.tasks'])


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
