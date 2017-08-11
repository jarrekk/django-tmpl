#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/08/2017
# email: me@jarrekk.com
from app_utils import rest_permission
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserList(APIView):
    """
    List all users, create a new user.
    """
    queryset = User.objects.none()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# todo
class Registration(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.initial_data['username'],
                email=serializer.initial_data['email'],
                first_name=serializer.initial_data['first_name'],
                last_name=serializer.initial_data['last_name']
            )
            user.set_password(serializer.initial_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# todo
class ResetPassword(APIView):
    pass


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.none()
    permission_classes = (rest_permission.UserOwnerOrAdmin, permissions.IsAuthenticated)

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
