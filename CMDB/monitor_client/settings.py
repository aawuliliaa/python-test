#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(BASE_DIR, "tmp")
database_host = "10.0.0.61"
database_user = "root"
database_password = "123"
database_name = "cmdb"
MY_THREAD_POOL_SIZE = 3