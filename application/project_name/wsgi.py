#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/3/17
# email: me@jarrekk.com

"""
WSGI settings for this project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

config = '.'.join(['settings', os.environ.get('ENV', 'development')])
os.environ['DJANGO_SETTINGS_MODULE'] = config

application = get_wsgi_application()

from .load import load_after_app_start

load_after_app_start()
