#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/3/17
# email: me@jarrekk.com
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
