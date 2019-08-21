#!/usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service.v1 import StarkHandler


class DepartmentHandler(StarkHandler):
    list_display = ['title', ]
