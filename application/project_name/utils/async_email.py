#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/7/17
# email: me@jarrekk.com
import logging
import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail as core_send_mail
from django.utils.log import AdminEmailHandler

logger = logging.getLogger('utils')


class AdminEmailThread(threading.Thread):
    def __init__(self, subject, message, fail_silently=False, html_message=None, connection=None):
        self.connection = connection
        self.subject = subject
        self.message = message
        self.recipient_list = [a[1] for a in settings.ADMINS]
        self.from_email = settings.SERVER_EMAIL
        self.fail_silently = fail_silently
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        if not settings.ADMINS:
            return
        mail = EmailMultiAlternatives('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, self.subject),
                                      self.message, settings.SERVER_EMAIL, [a[1] for a in settings.ADMINS],
                                      connection=self.connection)
        if self.html_message:
            mail.attach_alternative(self.html_message, 'text/html')
        try:
            mail.send(fail_silently=self.fail_silently)
        except Exception as e:
            logger.exception(e)


class AsyncAdminEmailHandler(AdminEmailHandler):
    def send_mail(self, subject, message, *args, **kwargs):
        AdminEmailThread(subject, message, *args, **kwargs).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, html_message, recipient_list, fail_silently, **kwargs):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.html_message = html_message
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.kwargs = kwargs
        threading.Thread.__init__(self)

    def run(self):
        try:
            core_send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                fail_silently=self.fail_silently,
                html_message=self.html_message,
                **self.kwargs)
        except Exception as e:
            logger.exception(e)


def send_mail(subject, message, from_email, html_message=None, recipient_list=[], fail_silently=False, **kwargs):
    EmailThread(subject, message, from_email, html_message, recipient_list, fail_silently, **kwargs).start()
