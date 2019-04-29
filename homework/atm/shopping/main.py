#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

from conf import settings
import os
from db.db_handler import load_db
from utils.print_log import print_info


def shopping_run(user_data):
    while 1:
        info = '''
        1.shopping
        2.show shopping history
        3.exit
        '''
        print_info(info)
        choice = input("please input your choice:").strip()
        choice_list = {
            "1": shopping,
            "2": show_shopping_history,
            "3": exit()
        }
        if choice in choice_list:
            choice_list[choice]()
        else:
            print_info("your input must be a number as showed before!","error")
        file = os.path.join(settings.GOODS_DATABASE["path"], '%s/%s.json' % (settings.GOODS_DATABASE["name"], "goods"))
        goods_data = load_db(file)
        print_info("***************goods info**************** ")
        for goods in goods_data:
            print_info("%s,%s,%s" % (goods_data.index(goods), goods["name"], goods["price"]))
        print_info("you can input one number to put it into shopping cart ")


def shopping():
    print_info()


def show_shopping_history():
    print_info()