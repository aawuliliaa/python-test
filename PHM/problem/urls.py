#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import re_path
from problem.views.performance import ProblemCountView, ProblemCountIndexView
app_name = "problem"
urlpatterns = [
    re_path(r'^json/problem_count/$', ProblemCountView.as_view(), name='problem_count_json'),
    re_path(r'^problem_count_index/$', ProblemCountIndexView.as_view(), name='problem_count'),
]
