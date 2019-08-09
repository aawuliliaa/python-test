#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import socket
import fcntl
import struct
import pymysql
import hashlib
from monitor_client import settings


def get_ip(ifname):
    """
    python的方式获取linux的本机IP
    :param ifname:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])


def get_conn():
    """
    返回pymysql的cursor
    :return:
    """
    # 链接
    conn = pymysql.connect(host=settings.database_host,
                           user=settings.database_user,
                           password=settings.database_password,
                           database=settings.database_name,
                           charset='utf8')
    # 游标
    # cursor=conn.cursor() #执行完毕返回的结果集默认以元组显示
    return conn


def get_table_name(name):
    """
    获取监控项对应的表名
    :param name:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(name.encode("utf-8"))
    table_name = "monitor_item_" + name + "_" + md5.hexdigest()[0:10]
    return table_name
