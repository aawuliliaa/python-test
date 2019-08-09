#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "monitor"
from django.urls import path
from django.contrib.auth.decorators import login_required
from monitor import views
# /monitor/monitor_item/
urlpatterns = [
    path('template/', login_required(views.TemplateView.as_view()), name="template"),
    path('add_template/', login_required(views.AddTemplate.as_view()), name="add_template"),
    path('del_template/<int:pk>/', login_required(views.DelTemplate.as_view()), name="del_template"),
    path('edit_template/<int:pk>/', login_required(views.EditTemplate.as_view()), name="edit_template"),

]
