#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib


def gen_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    ha = hashlib.md5(b'jk3usodfjwkrsdf')
    ha.update(origin.encode('utf-8'))
    return ha.hexdigest()
