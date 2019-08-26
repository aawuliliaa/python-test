#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from stark.service.StarkSite import site
from problem.views.problem import ProblemHandler
from problem.views.follow_up_record import FollowUpRecordHandler
from problem import models
site.register(models.Problem, ProblemHandler)
site.register(models.FollowUpRecord, FollowUpRecordHandler)