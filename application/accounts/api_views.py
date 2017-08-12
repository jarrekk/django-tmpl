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
from rest_framework import permissions
from rest_framework import status
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
    queryset = User.objects.none()
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        pk = request.data.get('pk', None)
        user = self.get_object(pk)
        if request.user.pk == user.pk:
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


class UserList(APIView):
    """
    List all users, create a new user.
    """
    queryset = User.objects.none()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = User.objects.none()
    permission_classes = (rest_framework_api.UserOwnerOrAdmin, permissions.IsAuthenticated)

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
            for k in serializer.initial_data.keys():
                if k == 'password':
                    user.set_password(serializer.initial_data['password'])
                    user.save()
                    continue
                try:
                    setattr(user, k, serializer.initial_data[k])
                except Exception as e:
                    logger.error(e)
                finally:
                    user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
