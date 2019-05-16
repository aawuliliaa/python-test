#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_LEVEL = logging.INFO
LOG_TYPES = {
    "client_log": "%s/log/client_log" % BASE_DIR
     }
FILE_STORAGE_PATH = "%s/file_storage" % BASE_DIR
TMP_FILE_PATH = "%s/tmp" % BASE_DIR
