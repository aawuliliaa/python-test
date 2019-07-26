#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.core.cache import cache
from asset import models


def get_data_from_cache(table_class_name):
    """
    由于会操作多个资产表，所以就通过反射的方式来写了
    由于是自己传入参数的，程序员在写代码的时候是能通过代码控制的，就不进行exception的判断了
    当然也可以进行补获异常
    :param table_class_name:
    :return:
    """
    # key为表名_obj_set
    cache_key = '{}_obj_set'.format(table_class_name)
    return_data_set = cache.get(cache_key)
    if return_data_set is None:
        # print('去数据库中查找数据')
        # 从models.py中获取该表名
        table_class = getattr(models, table_class_name)
        # 从表中获取数据
        return_data_set = table_class.objects.all()
        # print('将查询到的数据加载到缓存中')
        cache.set(cache_key, return_data_set)
    return return_data_set
