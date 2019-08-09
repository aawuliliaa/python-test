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
    path('monitor_item/', login_required(views.MonitorItemView.as_view()), name="monitor_item"),
    path('add_monitor_item/', login_required(views.AddMonitorItem.as_view()), name="add_monitor_item"),
    path('del_monitor_item/<int:pk>/', login_required(views.DelMonitorItem.as_view()), name="del_monitor_item"),
    path('edit_monitor_item/<int:pk>/', login_required(views.EditMonitorItem.as_view()), name="edit_monitor_item"),

]
