#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

import json


def save_db(file, data):
    """
    保存内容到文件中
    :param file:
    :param data:
    :return:
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_db(file):
    """
    加载数据，存到变量中
    :param file:
    :return:
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
