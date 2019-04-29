#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita


from utils.print_log import print_info
from utils.login_decorator import login_required

@login_required
def atm_run(user_data):
    choice = '''
       ------- Bank ---------
       1.  账户信息
       2.  还款
       3.  取款
       4.  转账
       5.  账单
       6.  退出
       '''
    print_info(choice)
    # choice_func = {
    #     "1": show_acount_info,
    #     "2": repay,
    #     "3": get_some_money,
    #     "4": transfer_to_others,
    #     "5": show_bill,
    #     "6": exit
    # }
