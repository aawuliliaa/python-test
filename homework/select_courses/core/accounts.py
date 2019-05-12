#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
from conf import settings
from utils.print_log import print_info
from core.db import DbHandler


class Account(object):
    """
    账户类，包含get和set方法，保存account对象和获取account对象
    """
    def __init__(self):
        self.username = None
        self.password = None
        # 分别为student teacher admin
        self.user_type = None

    def getter(self, username, user_type):
        """
        获取账号信息的时候可用
        :param username:
        :param user_type:
        :return:
        """
        if self.__check_user(username, user_type):
            db_handler = DbHandler(username, user_type, None)
            account_data = db_handler.get_data_from_db()
            return account_data

        return None

    def setter(self, username, password, user_type):
        """
        注册账号时使用
        :param username:
        :param password:
        :param user_type:
        :return:
        """
        if not self.__check_user(username, user_type):
            # 用户不存在，才进行下面的设置操作
            self.username = username
            self.password = password
            self.user_type = user_type
            return self

        # 用户存在，返回False
        return False

    @staticmethod
    def __check_user(username, user_type):
        """
        用于验证账户是否存在，由于用户类型不同，存在不同的路径，所以要传两个参数
        用户的账户文件是以用户名命名
        :param self:
        :param username:
        :param user_type:
        :return:
        """
        if os.path.exists("%s/%s" % (settings.ACCOUNT_PATH[user_type], username)):
            return True

        return False


class AdminAccount(Account):
    """
    管理员账户
    """
    def __init__(self):
        super(AdminAccount, self).__init__()

    def setter(self, username, password, user_type):
        set_result = super(AdminAccount, self).setter(username, password, user_type)
        if set_result:
            print_info("you are the first come to this system,"
                       "we will creat admin user for you!password is admin")
        return set_result


class StudentAccount(Account):
    """
    学生账户
    """
    def __init__(self):
        super(StudentAccount, self).__init__()
        self.associate_school_name = None
        self.associate_course_name = None
        self.associate_course_price = None
        self.associate_class_name = None
        self.associate_teacher_name = None
        self.record = None

    def setter(self, username, password, user_type):
        set_result = super(StudentAccount, self).setter(username, password, user_type)
        if set_result:
            return set_result

        return False


class TeacherAccount(Account):
    """
    老师类，用于创建老师账号
    """

    def __init__(self):
        super(TeacherAccount, self).__init__()
        self.associate_school_name = None
        # 创建班级的时候，分配了老师，假设一个老师管理好几个班级，所以这里用[]，可列出班级供老师选择
        self.classes = []

    def teacher_setter(self, username, password, user_type,  associate_school_name):
        set_result = super(TeacherAccount, self).setter(username, password, user_type)
        if set_result:
            self.associate_school_name = associate_school_name
            return self

        return False
