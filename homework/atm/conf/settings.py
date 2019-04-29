#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}
GOODS_DATABASE = {
    'engine': 'file_storage',
    'name': 'goods',
    'path': "%s/db" % BASE_DIR
}
LOG_LEVEL = logging.INFO
LOG_TYPES = {
    "login_log": "%s/log/login_log" % BASE_DIR,
    "transaction_log": "%s/log/transaction_log" % BASE_DIR,
     }
TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0},

}