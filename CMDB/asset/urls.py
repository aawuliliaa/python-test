#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "asset"
from django.urls import path
from asset import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('env/', login_required(views.Env.as_view()), name="env"),
]
