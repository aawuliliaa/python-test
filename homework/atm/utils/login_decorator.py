#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

# 只有用户登录了，才允许执行方法，否则，要从头开始，执行manage.py中的main


def login_required(func):
    def inner(*args, **kwargs):
        if args[0]["login"] == "yes":
            func(*args, **kwargs)
        else:
            #manage.main()
            print("you must login first")

    return inner

# 测试装饰器方法
@login_required
def test_dec(data):
    print(data)


test_dec({"user_name": "vita", "password": "1234567", "lock_status": "no", "login": "no"})



