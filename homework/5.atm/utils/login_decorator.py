#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita


def login_required(func):
    """
    只有用户登录了，才允许执行方法，否则，要从头开始，执行manage.py中的main
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        if args[0]["1.login"] == "yes":
            func(*args, **kwargs)
        else:
            # manage.main()
            print("you must 1.login first")

    return inner


@login_required
def test_dec(data):
    """
    测试装饰器方法
    :param data:
    :return:
    """
    print(data)


test_dec({"user_name": "vita", "password": "1234567", "lock_status": "no", "1.login": "no"})



