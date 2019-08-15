#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from permission import settings


def init_permission(request, current_user):
    """
    把当前登录用户能够访问的菜单放入session中
    用户访问其他页面时，从session中获取菜单信息
    :param request:
    :param current_user:
    :return:
    """
    # 当前用户所有权限
    # permissions__isnull=False是由于有的角色可能没有分配权限，此时permission处为null
    # 由于角色和权限是多对多关系，所以可能存在重复数据，需要distinct()去重
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__url",
                                                                                      "permissions__name",
                                                                                      "permissions__pid__id",
                                                                                      "permissions__pid__title",
                                                                                      "permissions__pid__url",
                                                                                      "permissions__menu__id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon"
                                                                                      ).distinct()

    # 3. 获取权限+菜单信息
    permission_dict = {}

    # {'customer_list': {'id': 1, 'title': '客户列表',
    #     'url': '/customer/list/', 'pid': None, 'p_title': None, 'p_url': None},
    # 'customer_add': {'id': 2, 'title': '添加客户',
    #     'url': '/customer/add/', 'pid': 1, 'p_title': '客户列表', 'p_url': '/customer/list/'},
    # 'payment_list': {'id': 7, 'title': '账单列表',
    #     'url': '/payment/list/', 'pid': None, 'p_title': None, 'p_url': None},
    # 'payment_add': {'id': 8, 'title': '添加账单',
    #     'url': '/payment/add/', 'pid': 7, 'p_title': '账单列表', 'p_url': '/payment/list/'}}
    menu_dict = {}
    # {1: {'title': '信息管理', 'icon': 'fa-fire', 'children': [{'title': '客户列表', 'url': '/customer/list/'}]},
    #  2: {'title': '用户管理', 'icon': 'fa-fire', 'children': [{'title': '账单列表', 'url': '/payment/list/'}]}}
    for item in permission_queryset:
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid__id'],
            'p_title': item['permissions__pid__title'],
            'p_url': item['permissions__pid__url'],
        }
        menu_id = item["permissions__menu__id"]
        if menu_id:
            node = {'id': item['permissions__id'], 'title': item['permissions__title'], 'url': item['permissions__url']}
            if menu_id in menu_dict:
                menu_dict[menu_id]["children"].append(node)
            else:
                menu_dict[menu_id] = {
                    'title': item['permissions__menu__title'],
                    'icon': item['permissions__menu__icon'],
                    'children': [node]
                }
    # print("----------------------------", menu_dict)
    # print("permission_dict------------",permission_dict)
    # {1: {'title': '信息管理', 'icon': 'fa-fire', 'children': [{'title': '客户列表', 'url': '/customer/list/'}]},
    #  2: {'title': '用户管理', 'icon': 'fa-fire', 'children': [{'title': '账单列表', 'url': '/payment/list/'}]}}
    # query_set不能直接放入session中,转换为列表，存入session中

    # 存入session中
    request.session[settings.SESSION_PERMISSION_URL] = permission_dict
    request.session[settings.SESSION_MENU_KEY] = menu_dict