#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

from conf import settings
from utils.print_log import print_info
from atm.transaction import transaction
from db.db_handler import load_db, save_db
from utils.login_decorator import login_required
import os


@login_required
def shopping_run(user_data):
    """
    购物的入口程序
    :param user_data:
    :return:
    """
    while True:
        info = '''
        ***************shopping choice****************
        1.shopping
        2.show shopping history
        3.exit
        ***************shopping choice****************
        '''
        print_info(info)
        choice_list = {
            "1": shopping,
            "2": show_shopping_history,
            "3": "exit"
        }
        your_choice = input("please input your choice:").strip()

        if your_choice in choice_list:
            if choice_list[your_choice] == "exit":
                exit()
            choice_list[your_choice](user_data)

        else:
            print_info("your input must be a number as showed before!", "error")


def shopping(user_data):
    """
    购物程序，调用transaction函数进行结账
    :param user_data:
    :return:
    """
    file = os.path.join(settings.GOODS_DATABASE["path"], '%s/%s.json' % (settings.GOODS_DATABASE["name"], "goods"))
    goods_data = load_db(file)
    print_info("***************goods info**************** ")
    for goods in goods_data:
        print_info("%s,%s,%s" % (goods_data.index(goods), goods["name"], goods["price"]))
    your_choice = input("you can input one number for shopping: ").strip()
    if your_choice.isdigit() and int(your_choice) < len(goods_data):
        your_choice = int(your_choice)
        goods_price = goods_data[your_choice]["price"]
        if transaction(user_data, goods_price, "consume"):
            goods_name = goods_data[your_choice]["name"]
            save_to_shop_history(user_data, goods_name, goods_price)
    else:
        print_info("your input is illegal!", "error")


def save_to_shop_history(user_data, goods_name, goods_price):
    """
    购物完成，保存到购物信息中
    :param user_data:
    :param goods_name:
    :param goods_price:
    :return:
    """
    user_name = user_data["user_name"]
    file = os.path.join(settings.GOODS_DATABASE["path"], '%s/shop_history_%s.json' %
                        (settings.GOODS_DATABASE["name"], user_name))
    if os.path.exists(file):
        shop_history_data = load_db(file)
        # shop_history_data = {
        #     "手机": {"price": "998", "count": 1},
        #     "裙子": {"price": "398", "count": 2},
        #     }
        if goods_name in shop_history_data:
            shop_history_data[goods_name]["count"] += 1
        else:
            shop_history_data[goods_name] = {}
            shop_history_data[goods_name]["price"] = goods_price
            shop_history_data[goods_name]["count"] = 1
    else:
        shop_history_data = dict()
        shop_history_data[goods_name] = {}
        shop_history_data[goods_name]["price"] = goods_price
        shop_history_data[goods_name]["count"] = 1
    save_db(file, shop_history_data)
    print_info("you have shopped %s" % goods_name)


def show_shopping_history(user_data):
    """展示购物历史信息"""
    user_name = user_data["user_name"]
    file = os.path.join(settings.GOODS_DATABASE["path"], '%s/shop_history_%s.json' %
                        (settings.GOODS_DATABASE["name"], user_name))
    if os.path.exists(file):
        shopping_history_data = load_db(file)
        print_info("************1.shop history****************")
        for goods_name in shopping_history_data:

            goods_price = shopping_history_data[goods_name]["price"]
            goods_count = shopping_history_data[goods_name]["count"]
            print_info("%s,%s,%s" % (goods_name, goods_price, goods_count))
        print_info("************1.shop history****************")
    else:
        print_info("this user has never shopped something!", "error")
