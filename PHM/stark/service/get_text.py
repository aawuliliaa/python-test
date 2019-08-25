#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita


def get_choice_text(title, field):
    """
    对于Stark组件中定义列时，choice如果想要显示中文信息，调用此方法即可。
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :return:
    """

    def inner(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return title
        method = "get_%s_display" % field
        return getattr(obj, method)()

    return inner


def get_datetime_text(title, field, time_format='%Y-%m-%d'):
    """
    对于Stark组件中定义列时，定制时间格式的数据
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :param time_format: 要格式化的时间格式
    :return:
    """

    def inner(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return title
        datetime_value = getattr(obj, field)
        if datetime_value is None:
            return ""
        else:
            return datetime_value.strftime(time_format)

    return inner


def get_m2m_text(title, field):
    """
    对于Stark组件中定义列时，显示m2m文本信息
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :param time_format: 要格式化的时间格式
    :return:
    """

    def inner(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return title
        queryset = getattr(obj, field).all()
        text_list = [str(row) for row in queryset]
        return ','.join(text_list)

    return inner