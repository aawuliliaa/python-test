#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import logging
from conf import settings


def return_logger_obj(log_type):
    """
    主要用于返回logger对象，让用户输出日志到文件中
    :log_type: 该变量可用于创建log文件和输出日志中的提示信息
    :return:logger 对象
    """
    file_handler = logging.FileHandler(settings.LOG_TYPES[log_type])
    file_handler.setLevel(settings.LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(file_handler)
    return logger


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
