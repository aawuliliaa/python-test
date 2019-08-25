#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from stark.service.StarkHandler import StarkHandler


class ProblemHandler(StarkHandler):
    list_display = ["desc", "detail", "create_person", "deal_person",
                    "create_time", "start_deal_time", "stop_deal_time", "status"]