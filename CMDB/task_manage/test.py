#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from crond.tasks import *
t1 = add.delay(45,2)
print(t1.get()) #获取执行的结果