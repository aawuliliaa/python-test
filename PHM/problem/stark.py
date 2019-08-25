#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from stark.service.StarkSite import site
from problem.views.problem import ProblemHandler
from problem import models
site.register(models.Problem, ProblemHandler)