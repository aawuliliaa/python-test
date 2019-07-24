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
    path('system/', login_required(views.SystemView.as_view()), name="system"),
    path('add_system/', login_required(views.AddSystem.as_view()), name="add_system"),
    path('del_system/<int:pk>/', login_required(views.DelSystem.as_view()), name="del_system"),
    path('edit_system/<int:pk>/', login_required(views.EditSystem.as_view()), name="edit_system"),
    path('application/', login_required(views.ApplicationView.as_view()), name="application"),
    path('add_application/', login_required(views.AddApplication.as_view()), name="add_application"),
    path('del_application/<int:pk>/', login_required(views.DelApplication.as_view()), name="del_application"),
    path('edit_application/<int:pk>/', login_required(views.EditApplication.as_view()), name="edit_application"),
]
