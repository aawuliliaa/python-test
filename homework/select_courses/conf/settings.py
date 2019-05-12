#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNT_PATH = {'student': "%s/db/accounts/student" % BASE_DIR,
                'teacher': "%s/db/accounts/teacher" % BASE_DIR,
                'admin': "%s/db/accounts/admin" % BASE_DIR
                }
SCHOOL_PATH = "%s/db/school" % BASE_DIR
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "admin"
LOG_LEVEL = logging.INFO
LOG_TYPES = {
    "access_log": "%s/log" % BASE_DIR
     }