#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 8/4/17
# email: me@jarrekk.com
import logging

from django.views import generic

logger = logging.getLogger('views')


class IndexView(generic.TemplateView):
    """
    index page views
    """
    template_name = 'index.html'
    v = 'index page'

    def get_context_data(self, **kwargs):
        logger.info('generic views.')
        return {'v': self.v}
