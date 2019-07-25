#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "crond"
from django.urls import path
from django.contrib.auth.decorators import login_required
from crond import views

urlpatterns = [
    path('crontab_schedule/', login_required(views.CrontabScheduleView.as_view()), name="crontab_schedule"),
    path('add_crontab_schedule/', login_required(views.AddCrontabSchedule.as_view()), name="add_crontab_schedule"),
    path('del_crontab_schedule/<int:pk>/', login_required(views.DelCrontabSchedule.as_view()), name="del_crontab_schedule"),
]
