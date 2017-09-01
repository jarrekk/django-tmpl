#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/3/17
# email: me@jarrekk.com
import logging

from app_utils.tokens import account_activation_token
from django.contrib.auth import login
from .models import User
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import generic

logger = logging.getLogger('views')


class ActivateView(generic.View):
    """
    Activate page
    """

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uid64']))
            user = User.objects.get(pk=uid)
        except Exception as e:
            logger.info(e)
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            email_address = user.emailaddress_set.first()
            email_address.verified = True
            email_address.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponse('Activation link is invalid!')
