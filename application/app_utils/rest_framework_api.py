#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/08/2017
# email: me@jarrekk.com
from rest_framework import permissions
from accounts.serializers import UserSerializer

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
