#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from views import *
url_patterns=[
    ("/index", index),
    ("/login", login),
    ("/favicon.ico", favicon),
    ("/auth", auth)
]