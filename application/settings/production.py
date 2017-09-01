#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/3/17
# email: me@jarrekk.com
from .base import *

# logging configure
# todo add sentry config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'app_utils.async_email.AsyncAdminEmailHandler',
            'include_html': True,
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(ROOT_DIR.path('django.log')),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 2,
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(pathname)s %(funcName)s %(lineno)d--%(message)s',
            'datefmt': "%Y-%b-%d %H:%M:%S"
        }
    },
    'loggers': {
        'tasks': {
            'handlers': ['logfile', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'models': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'utils': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'views': {
            'handlers': ['console', 'logfile', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

logging.config.dictConfig(LOGGING)
