#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 12/08/2017
# email: me@jack003.com
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()
