#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
import string
# 字节
#data = "0.98G".replace("[G]","").replace(".","").isdigit()
data = "0.98G".replace("G","")

print(float(data)*1024*1024)
#1M*1024*1024