#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import hashlib
import pymysql


def get_table_name(name):
    """
    根据监控项name获取表名
    :param name:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(name.encode("utf-8"))
    table_name = "monitor_item_" + name + "_" + md5.hexdigest()[0:10]
    return table_name


def get_pymysql_conn():
    """
    返回数据库连接
    :return:
    """
    # 链接
    conn = pymysql.connect(host='10.0.0.61',
                           user='root',
                           password='123',
                           database='cmdb',
                           charset='utf8')
    return conn