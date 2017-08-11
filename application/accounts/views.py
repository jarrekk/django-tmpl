#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/3/17
# email: me@jarrekk.com
import logging

from app_utils.tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

logger = logging.getLogger('views')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        emailaddress = user.emailaddress_set.first()
        emailaddress.verified = True
        emailaddress.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
