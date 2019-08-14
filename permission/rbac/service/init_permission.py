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
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                      'permissions__title',
                                                                                      'permissions__url',
                                                                                      'permissions__is_menu',
                                                                                      'permissions__icon'
                                                                                      ).distinct()
    print("---------------", permission_queryset)
    # permission_set = models.Permission.objects.filter(role__userinfo__name=user)
    # print("---------------",permission_set)

    # 获取权限中所有的URL
    permission_list = []
    menu_list = []
    for item in permission_queryset:
        permission_list.append(item['permissions__url'])
        if item["permissions__is_menu"]:
            tmp = {
                'title': item['permissions__title'],
                'icon': item['permissions__icon'],
                'url': item['permissions__url']
            }
            menu_list.append(tmp)
    # query_set不能直接放入session中,转换为列表，存入session中

    # 存入session中
    request.session[settings.SESSION_PERMISSION_URL_LIST] = permission_list
    request.session[settings.SESSION_MENU_KEY] = menu_list