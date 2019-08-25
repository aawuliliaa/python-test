#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from stark.service.StarkHandler import StarkHandler
from stark.service.get_text import *
from stark.service.StarkHandler import Option


class ProblemHandler(StarkHandler):
    list_display = [StarkHandler.display_checkbox, "desc", "detail", "create_person", "deal_person",
                    get_datetime_text("问题创建时间", "create_time", time_format='%Y-%m-%d %H:%I:%M'),
                    get_datetime_text("问题开始处理时间", "start_deal_time"),
                    get_datetime_text("问题完成时间", "stop_deal_time"), get_choice_text("状态", "status")]
    search_list = ['detail', 'desc', ]
    order_list = ["-id"]
    action_list = [StarkHandler.action_multi_delete]
    search_group = [
        Option('status'),
    ]