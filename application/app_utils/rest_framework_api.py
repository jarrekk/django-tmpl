#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/08/2017
# email: me@jarrekk.com
from accounts.serializers import UserSerializer
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from rest_framework import permissions


# Custom rest_framework permission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class UserOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # User should be active
        if not request.user.is_active:
            return False

        # Superuser can control any user
        if request.user.is_superuser:
            return True
        elif request.user.emailaddress_set.exists():
            return request.user.id == obj.id and request.user.emailaddress_set.first().verified
        else:
            return request.user.id == obj.id

# Custom rest_framework jwt response


def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

# Pagination for APIView


def paginator(request, queryset):
    full_path = request.build_absolute_uri('?')
    parameters = request.GET
    per_page = parameters.get('per_page', settings.PER_PAGE)
    try:
        page = int(parameters.get('page', None))
    except TypeError:
        page = 1
    count = queryset.count()

    pagination = Paginator(queryset, per_page)

    try:
        queryset = pagination.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = pagination.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = pagination.page(pagination.num_pages)

    # next & previous url
    url_next, url_previous = None, None
    if queryset.has_next():
        parameters_next = parameters.copy()
        parameters_next['page'] = page + 1
        url_next = '?'.join([full_path, parameters_next.urlencode()])

    if queryset.has_previous():
        parameters_previous = parameters.copy()
        parameters_previous['page'] = page + 1
        url_previous = '?'.join([full_path, parameters_previous.urlencode()])

    return queryset, url_next, url_previous, count

# Filter for APIView


def sort_filter(queryset, serializer_class, request, logger):
    parameters = dict(request.GET.copy())
    # sort
    sortby = None
    if getattr(serializer_class.Meta, 'sort_fields', None):
        sort_fields = getattr(serializer_class.Meta, 'sort_fields')
        if parameters.get('sortby', None) and parameters['sortby'][-1] in sort_fields:
            sortby = parameters.get('sortby')[-1]
    order = '-' if parameters.get('order', None) and parameters.get('order')[-1] == 'desc' else ''
    sort = order + sortby if sortby else None
    queryset = queryset.order_by(sort) if sort else queryset
    # filter
    parameters = {k: v[-1] for k, v in parameters.items() if k not in ['page', 'per_page', 'sortby', 'order']}
    try:
        queryset = queryset.filter(**parameters)
    except Exception as e:
        logger.info(e)
        raise Http404
    return queryset, sort, parameters.keys() if parameters else None
