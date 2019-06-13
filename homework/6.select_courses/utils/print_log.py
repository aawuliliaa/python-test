#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita


def print_info(info, log_type="info"):
    """
    输出提示信息！
    :param info: 输入要输出的提示信息
    :param log_type: 根据log_type的不同，提示信息的颜色不同
    :return:
    """
    if log_type == "info":
        print("\033[32;1m %s \033[0m" % info)
    else:
        print("\033[31;1m %s \033[0m" % info)
