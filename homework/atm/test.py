#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from auth.login import user_login, shopping_or_atm
from utils.login_decorator import login_required
import time,datetime
#{"user_name":"vita","password":"1234567","lock_status":"no"}
# @login_required
# def test_dec(data):
#     print(data)
#
#
# test_dec({"user_name": "vita", "password": "1234567", "lock_status": "no", "login": "no"})
print(datetime.datetime.now() + datetime.timedelta(5*365))

print(time.strftime("%Y-%m-%d", time.gmtime()))
#print(time.strftime(time.strptime(datetime.datetime.now() + datetime.timedelta(5*365),"%Y-%m-%d") ))