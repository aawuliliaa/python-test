#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from core.accounts import Account
from utils.print_log import print_info
from core.school import School


class View:
    account = Account()
    school_obj = School()

    def __init__(self):
        # 登录的时候，会设置这个变量，后面获取用户的对象，都从这里获取
        # 保存登录状态
        self.user_data = {
                 'is_authenticated': False,
                 'account_data': None,
                 }

    def login(self, user_type):
        """
        登录函数
        :param user_type:
        :return:
        """
        exit_flag = True
        while exit_flag:
            if not self.user_data["is_authenticated"]:
                username = input("input your name:").strip()
                password = input("input password:").strip()
                account_data = self.account.getter(username, user_type)
                if account_data is not None and account_data.user_type == user_type:
                    if account_data.password == password and account_data.username == username:
                        print_info("1.login success!")
                        # 保存登录用户的对象到user_data中
                        self.user_data["is_authenticated"] = True
                        self.user_data["account_data"] = account_data
                        return True
                    else:
                        print_info("username or password is not correct!", "error")
                        exit_flag = False
                else:
                    print_info("there is something wrong with your username or user_type", "error")
                    exit_flag = False
            else:
                return True

    def log_out(self):
        """
        可用于老师登录，学生登录，管理员登录之后的退出登录，进入初始页面的操作。
        :return:
        """
        if self.user_data["is_authenticated"]:
            username = self.user_data["account_data"].username
            self.user_data = {
                "is_authenticated": False,
                "account_data": None
            }
            print_info("%s logout successful!" % username)







