#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/08/2017
# email: me@jarrekk.com
from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, default=None)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
