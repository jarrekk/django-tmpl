#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/08/2017
# email: me@jarrekk.com
import logging

from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress
from app_utils import rest_framework_api
from app_utils.async_email import send_mail
from app_utils.tokens import account_activation_token
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import UserSerializer

logger = logging.getLogger('views')


class SendEmailClass(object):

    @staticmethod
    def active_email(request, user):
        message = render_to_string('email/active_email.txt', {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        subject = 'Activate your blog account.'
        to_email = user.email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list=[to_email])


class Registration(generics.CreateAPIView, SendEmailClass):
    """
    User registration
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.initial_data['username'],
            email=serializer.initial_data['email'],
            first_name=serializer.initial_data['first_name'],
            last_name=serializer.initial_data['last_name']
        )
        user.set_password(serializer.initial_data['password'])
        user.save()
        EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)
        # send email
        self.active_email(request, user)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data.update({'id': user.pk})
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ResendActiveEmail(generics.RetrieveUpdateAPIView, SendEmailClass):
    """
    If user doesn't receive active email, resend an email.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    http_method_names = ['put', 'patch']
    exclude_from_schema = False

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.pk == self.request.user.pk:
            if instance.emailaddress_set.first().verified:
                return Response({'detail': 'User is activated.'}, status=status.HTTP_400_BAD_REQUEST)
            # send email
            self.active_email(self.request, instance)
            return Response({'detail': 'An email has been sent to your email address.'})
        return Response({'detail': 'You do not have permission to perform this action.'})


class ResetPassword(generics.CreateAPIView):
    """
    User reset password with email.
    """
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        formset = ResetPasswordForm(request.data)
        if formset.is_valid():
            formset.save(request)
            return Response({'detail': 'An email has been sent to your email address.'})
        return Response({'detail': 'Email was not provided or error.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.UpdateAPIView,):
    """
    User change password.
    :parameter
    old_password string
    password string
    """
    queryset = User.objects.all()
    permission_classes = (rest_framework_api.UserOwnerOrAdmin, permissions.IsAuthenticated)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_password = request.data.get('old_password', None)
        password = request.data.get('password', None)
        if not old_password:
            return Response({'detail': 'Old password was not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'detail': 'Password was not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        if instance.check_password(old_password):
            serializer = self.get_serializer(instance, data={'password': password}, partial=True)
            serializer.is_valid(raise_exception=True)
            instance.set_password(password)
            instance.save()
            return Response(serializer.data)
        return Response({'detail': 'Old password error.'}, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    """
    List all users.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    filter_fields = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'email')
    ordering_fields = ('id', 'username', 'email')
    ordering = ('id',)

    def list(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    permission_classes = (rest_framework_api.UserOwnerOrAdmin, permissions.IsAuthenticated)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # User can't update password with this API
        self.serializer_class.Meta.fields = ('id', 'username', 'first_name', 'last_name', 'email')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
