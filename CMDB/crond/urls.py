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
    path('interval_schedule/', login_required(views.IntervalScheduleView.as_view()), name="interval_schedule"),
    path('add_interval_schedule/', login_required(views.AddIntervalSchedule.as_view()), name="add_interval_schedule"),
    path('del_interval_schedule/<int:pk>/', login_required(views.DelIntervalSchedule.as_view()), name="del_interval_schedule"),
    path('periodic_tasks/', login_required(views.PeriodicTasksView.as_view()), name="periodic_tasks"),
    path('add_periodic_tasks/', login_required(views.AddPeriodicTasks.as_view()), name="add_periodic_tasks"),
    path('edit_periodic_tasks/<int:pk>/', login_required(views.EditPeriodicTasks.as_view()), name="edit_periodic_tasks"),
    path('del_periodic_tasks/<int:pk>/', login_required(views.DelPeriodicTasks.as_view()),name="del_periodic_tasks"),
]
