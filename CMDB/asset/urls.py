#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "asset"
from django.urls import path
from asset import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('env/', login_required(views.Env.as_view()), name="env"),
    path('add_env/', login_required(views.AddEnv.as_view()), name="add_env"),
    path('del_env/<int:pk>/', login_required(views.DelEnv.as_view()), name="del_env"),
    path('edit_env/<int:pk>/', login_required(views.EditEnv.as_view()), name="edit_env"),
]
