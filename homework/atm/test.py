#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from auth.login import user_login, shopping_or_atm
from utils.login_decorator import login_required
import re
import json
import os
from conf import settings

#file = os.path.join(settings.GOODS_DATABASE["path"], '%s/%s.json' % (settings.GOODS_DATABASE["name"], "shop_history"))


with open(file="test.json",mode="w",encoding="utf-8") as f:
    data = {"电脑":"哈哈"}
    json.dump(data,f)

