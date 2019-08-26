#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from sign.models import UserInfo


def dev_ops_user_dict():
    user_id_list = []
    user_name_list = []
    ops_user_set = UserInfo.objects.filter(roles__title="devops")
    for ops_user_obj in ops_user_set:
        user_name_list.append(ops_user_obj.name)
        user_id_list.append(ops_user_obj.id)
    return {"user_id_list": user_id_list, "user_name_list": user_name_list}