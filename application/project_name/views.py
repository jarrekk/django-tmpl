#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/4/17
# email: me@jarrekk.com
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import View

logger = logging.getLogger('views')


class Index(View):
    """
    index page views
    """
    v = 'index page'

    def get(self, request):
        logger.info('index log')
        v = self.v
        return render_to_response('index.html', locals(), RequestContext(request))
