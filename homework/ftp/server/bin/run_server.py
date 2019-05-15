#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
import sys
# 需要把server目录加入到环境变量，后面才能使用from core import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from core.management import Management
    # 默认不加参数时，sys.argv=['E:/PythonProject/python-test/homework/ftp/server/bin/run_server.py']
    manage_obj = Management(sys.argv)
    manage_obj.run()
