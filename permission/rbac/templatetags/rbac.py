#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.template import Library
from collections import OrderedDict
from django.conf import settings

register = Library()
@register.inclusion_tag("rbac/menu.html")
def menu(request):
    menu_list = request.session.get(settings.SESSION_MENU_KEY)
    for item in menu_list:
        if re.match(item["url"], request.path_info):
            item["class"] = "active"
    #         注意这里的返回值，要是字典，前端直接循环menu_list
    return {
        'menu_list': request.session.get(settings.SESSION_MENU_KEY)
    }


@register.inclusion_tag("rbac/multi_menu.html")
def multi_menu(request):
    menu_dict = request.session.get(settings.SESSION_MENU_KEY)
    # {1: {'title': '信息管理', 'icon': 'fa-fire', 'children': [{'title': '客户列表', 'url': '/customer/list/'}]},
    #  2: {'title': '用户管理', 'icon': 'fa-fire', 'children': [{'title': '账单列表', 'url': '/payment/list/'}]}}
    # 对字典的key进行排序

    #空的有序字典
    ordered_dict = OrderedDict()
    key_list = sorted(menu_dict)
    for key in key_list:
        val = menu_dict[key]
        val['class'] = "hide"

        for per in val['children']:
            if re.match(per['url'], request.path_info):
                per['class'] = 'active'
                # 父菜单去掉hide
                val['class'] = ''
        ordered_dict[key] = val
    #         注意这里的返回值，要是字典，前端直接循环menu_list
    return {
        'menu_dict': request.session.get(settings.SESSION_MENU_KEY)
    }