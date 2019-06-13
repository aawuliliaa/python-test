#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import pickle
from conf.settings import ACCOUNT_PATH, SCHOOL_PATH


class DbHandler(object):
    """
    用于操作用户数据文件
    """
    def __init__(self, username, user_type, data):
        self.file = "%s/%s" % (ACCOUNT_PATH[user_type], username)
        self.data = data

    def save_to_db(self):
        """
        保存数据到文件中
        :return:
        """
        with open(self.file, "wb") as f:
            pickle.dump(self.data, f)

    def get_data_from_db(self):
        """
        获取数据
        :return:
        """
        with open(self.file, "rb") as f:
            self.data = pickle.load(f)
            return self.data


class SchoolDbHandler(DbHandler):
    """
    用于操作学校的数据文件
    """
    def __init__(self, school_name, school_data):
        self.file = "%s/%s" % (SCHOOL_PATH, school_name)
        self.data = school_data

