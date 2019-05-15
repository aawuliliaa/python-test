#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import logging
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_LEVEL = logging.INFO
LOG_TYPES = {
    "server_log": "%s/log/server_log" % BASE_DIR
     }
FTP_SERVER_HOST = "127.0.0.1"
FTP_SERVER_PORT = 9999
ACCOUNT_FILE = "%s/conf/account.ini" % BASE_DIR
USER_HOME_DIR = "%s/home" % BASE_DIR
