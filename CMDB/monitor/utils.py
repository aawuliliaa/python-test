#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import hashlib
def get_table_name(name):
    md5 = hashlib.md5()
    md5.update(name.encode("utf-8"))
    table_name = "monitor_item_" + name + "_" + md5.hexdigest()[0:10]
    return table_name