#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from utils.print_log import print_info
from utils.login_decorator import login_required
from atm.transaction import transaction
from conf import settings
from db.db_handler import load_db
import re
import os


@login_required
def atm_run(user_data):
    """
    atm程序的入口，可以进行一些转账，还款的操作
    :param user_data:
    :return:
    """
    while 1:

        choice = '''
           ------- Bank ---------
           1.  账户信息
           2.  还款
           3.  取款
           4.  转账
           5.  账单
           6.  退出
           ------- Bank ---------
           '''
        choice_list = {
            "1": show_account_info,
            "2": repay,
            "3": withdraw,
            "4": transfer,
            "5": show_bill,
            "6": "exit"
        }
        print_info(choice)
        your_choice = input("please input your choice:").strip()
        if your_choice in choice_list:
            if choice_list[your_choice] == "exit":
                exit()
            choice_list[your_choice](user_data)
        else:
            print_info("your input is illegal!")


def show_account_info(user_data):
    """
    显示用户的账户信息
    :param user_data:
    :return:
    """
    print_info("*************account info***************")
    for key, value in user_data.items():

        print_info("%15s:%s" % (key, value))
    print_info("*************account info***************")


def repay(user_data):
    """
    还款功能
    :param user_data:
    :return:
    """
    repay_money = input("input money you want to repay:").strip()
    # 匹配数字，包含小数，因为"12.23".isdigit()是false,这里通过正则表达式来进行匹配
    if re.match("^[0-9]+[.]?[0-9]*$", repay_money):
        # user_data["left_credit"] += repay_money
        transaction(user_data, repay_money, "repay")
    else:
        print_info("your input is illegal!", "error")


def withdraw(user_data):
    """
    取款
    :param user_data:
    :return:
    """
    withdraw_money = input("input money you want to withdraw:").strip()
    # 匹配数字，包含小数，因为"12.23".isdigit()是false,这里通过正则表达式来进行匹配
    if re.match("^[0-9]+[.]?[0-9]*$", withdraw_money):
        # user_data["left_credit"] -= withdraw_money
        transaction(user_data, withdraw_money, "withdraw")
    else:
        print_info("the money your input is illegal!", "error")


def transfer(user_data):
    """
    转账
    :param user_data:
    :return:
    """
    transfer_user_name = input("input the user name you want to transfer:").strip()
    transfer_money = input("input the money you want to transfer:").strip()
    transfer_user_file = os.path.join(settings.DATABASE["path"], '%s/%s.json' %
                                      (settings.DATABASE["name"], transfer_user_name))
    if os.path.isfile(transfer_user_file):
        if re.match("^[0-9]+[.]?[0-9]*$", transfer_money):
            # 当前用户减去传输的金额
            transaction(user_data, transfer_money, "transfer")
            # 另一个用户加上传输的金额
            transfer_user_data = load_db(transfer_user_file)
            transaction(transfer_user_data, transfer_money, "repay")
        else:
            print_info("the money your input is illegal!", "error")
    else:
        print_info("transfer user is not exist!", "error")


def show_bill(user_data):
    """
    显示当前登录人的账单
    :param user_data:
    :return:
    """
    transaction_log_file = settings.LOG_TYPES["transaction_log"]
    f = open(file=transaction_log_file, mode="r", encoding="utf-8")
    for line in f:
        # 取出当前登录用户的账单
        if line.split("account:")[1].split("action")[0].strip() == user_data["user_name"]:
            print_info(line)

