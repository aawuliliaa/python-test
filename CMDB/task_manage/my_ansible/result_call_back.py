#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: vita
# 状态回调，各种成功失败的状态
from ansible.plugins.callback import CallbackBase


class CallbackResultCollector(CallbackBase):
    """
    callback改写，格式化输出playbook执行结果
    """
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_unreachable = {}
        self.task_failed = {}
        self.task_skipped = {}
        self.task_status = {}

    def v2_runner_on_unreachable(self, result):
        """
        重写 unreachable 状态
        :param result:  这是父类里面一个对象，这个对象可以获取执行任务信息
        """
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """
        重写 ok 状态
        :param result:
        """
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        """
        重写 failed 状态
        :param result:
        """
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()] = result