#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from utils.print_log import print_info, return_logger_obj
from conf import settings
import os
from db.db_handler import save_db


def transaction(user_data, money, tran_type):
    if tran_type in settings.TRANSACTION_TYPE:
        money = float(money)
        action = settings.TRANSACTION_TYPE[tran_type]["action"]
        interest = money*settings.TRANSACTION_TYPE[tran_type]["interest"]
        if action == "plus":
            user_data["left_credit"] = user_data["left_credit"] + money - interest

        elif action == "minus":
            user_data["left_credit"] = user_data["left_credit"] - money - interest
            if user_data["left_credit"] < 0:
                print_info("the money you left is not enough!")
                return None
        print_info("transaction successful!")
        user_file = os.path.join(settings.DATABASE["path"], '%s/%s.json' %
                                 (settings.DATABASE["name"], user_data["user_name"]))
        save_db(user_file, user_data)
        logger = return_logger_obj("transaction_log")
        logger.info("account:%s   action:%s    amount:%s   interest:%s" %
                    (user_data["user_name"], tran_type, money, interest))
