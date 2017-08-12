#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 12/08/2017
# email: me@jack003.com
from django.contrib.auth.models import User


def LoadAfterAPPStart():
    User._meta.get_field('email')._unique = True
