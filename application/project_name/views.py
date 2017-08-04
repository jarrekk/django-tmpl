#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/4/17
# email: me@jarrekk.com
from django.shortcuts import render_to_response
import logging

logger = logging.getLogger('views')


def index(request):
    logger.info('index log')
    return render_to_response('index.html')
