#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import path
from sign.views import sign_action
app_name = "sign"
urlpatterns = [
path('index/', sign_action.index, name="index"),
    path('login/', sign_action.login, name="login"),
    path('register/', sign_action.register, name="register"),
    path('logout/', sign_action.logout, name="logout"),
]
