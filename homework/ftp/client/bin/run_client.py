#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    from core.ftpclient import FtpClient
    ftp_client_obj = FtpClient()
    ftp_client_obj.interactive()