#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import re_path
from problem.views.performance import ProblemCountJsonView, ProblemCountIndexView, \
    ProblemDealTimeIndexView, ProblemDealTimeJsonView, ProblemEfficientIndexView, ProblemEfficientJsonView
app_name = "problem"
urlpatterns = [
    re_path(r'^json/problem_count/$', ProblemCountJsonView.as_view(), name='problem_count_json'),
    re_path(r'^problem_count_index/$', ProblemCountIndexView.as_view(), name='problem_count'),
    re_path(r'^json/problem_deal_time/$', ProblemDealTimeJsonView.as_view(), name='problem_deal_time_json'),
    re_path(r'^problem_deal_time_index/$', ProblemDealTimeIndexView.as_view(), name='problem_deal_time'),
    re_path(r'^json/problem_efficient_time/$', ProblemEfficientJsonView.as_view(), name='problem_efficient_time_json'),
    re_path(r'^problem_efficient_index/$', ProblemEfficientIndexView.as_view(), name='problem_efficient_time'),
]
