#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/08/2017
# email: me@jarrekk.com
from accounts.serializers import UserSerializer
from rest_framework import pagination
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
    message = 'You do not have permission to perform this action.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # User should be active
        if not request.user.is_active:
            self.message = 'User is not active.'
            return False

        # Superuser can control any user
        if request.user.is_superuser:
            return True
        if request.user.pk != obj.pk:
            return False
        if request.user.emailaddress_set.exists() and not request.user.emailaddress_set.first().verified:
            self.message = 'Please activate your user via confirm email.'
            return False
        return True

# Custom rest_framework jwt response


def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
