#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "task_manage"
from django.urls import path
from django.contrib.auth.decorators import login_required
from task_manage import views

urlpatterns = [
    path('webssh_login/', login_required(views.WebsshLogin.as_view()), name="webssh_login"),

]
