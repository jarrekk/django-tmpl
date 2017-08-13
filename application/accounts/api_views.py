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
from django.http import Http404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

logger = logging.getLogger('views')


class Registration(APIView):
    """
    User registration
    """
    permission_classes = (permissions.AllowAny,)

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

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() and serializer.initial_data.get('password', None):
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendActiveEmail(Registration):
    """
    If user doesn't receive active email, resend an email.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            user = self.queryset.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except Exception as e:
            logger.info(e)
            raise Http404

    def post(self, request, format=None):
        pk = request.data.get('pk', None)
        user = self.get_object(pk)

        if request.user.pk == user.pk:
            if user.emailaddress_set.first().verified:
                return Response({'detail': 'User is activated.'}, status=status.HTTP_400_BAD_REQUEST)
            # send email
            self.active_email(request, user)
            return Response({'detail': 'An email has been sent to your email address.'})
        return Response({'detail': 'You do not have permission to perform this action.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
    User reset password with email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        formset = ResetPasswordForm(request.data)
        if formset.is_valid():
            formset.save(request)
            return Response({'detail': 'An email has been sent to your email address.'})
        return Response({'detail': 'Email was not provided.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (rest_framework_api.UserOwnerOrAdmin, permissions.IsAuthenticated)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        password = request.data.get('password', None)
        if password:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            instance.set_password(password)
            instance.save()
            return Response(serializer.data)
        return Response({'detail': 'Password was not provided.'}, status=status.HTTP_400_BAD_REQUEST)


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
