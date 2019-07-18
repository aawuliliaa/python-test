#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.shortcuts import HttpResponse
import csv
import codecs
from web.models import *


def get_label(request):
    """
    base中左侧导航处的菜单
    :param request:
    :return:
    """
    # 获取当前用户的email
    email = request.user.email
    # 查找当前用户的左侧菜单和URL信息
    # 由于用户和角色是多对多的关系，可能出现下面的情况，但是字典是不重复的，所以自动去重了
    # role1 pa_menu1 child_menu1 url1
    # role2 pa_menu1 child_menu1 url1
    if request.user.is_admin:
        role_set_list = Role.objects.all()
    else:
        role_set_list = Role.objects.filter(users__email=email).all()
    left_label_dic = {}

    for role_obj in role_set_list:
        left_label_dic[role_obj.parent_menu_name] = {}
    for role_obj in role_set_list:
        left_label_dic[role_obj.parent_menu_name][role_obj.child_menu_name] = role_obj.url
    # ret = {'资产信息': {'系统信息': '/system/', '环境信息': '/env/', '主机信息': '/host/'}}
    # 共有四次SQL查询
    # b'SELECT * FROM `web_myuser` WHERE `web_myuser`.`id` = 37';args=(37,)
    # b'SELECT * FROM `web_myuser` WHERE `web_myuser`.`id` = 37';args=(37,)

    # b"SELECT * FROM `web_role` INNER JOIN `web_role_users` ON (`web_role`.`id` = `web_role_users`.`role_id`)
    # INNER
    # JOIN
    # `web_myuser`
    # ON(`web_role_users`.
    # `myuser_id` = `web_myuser`.
    # `id`) WHERE
    # `web_myuser`.
    # `email` = 'cc@qq.com'"; args=('cc@qq.com',)

    # b"SELECT * FROM `web_role` INNER JOIN `web_role_users` ON (`web_role`.`id` = `web_role_users`.`role_id`)
    # INNER
    # JOIN
    # `web_myuser`
    # ON(`web_role_users`.
    # `myuser_id` = `web_myuser`.
    # `id`) WHERE
    # `web_myuser`.
    # `email` = 'cc@qq.com'"; args=('cc@qq.com',)

    return left_label_dic


def export(filename, export_datas, header):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(
        response,
        dialect='excel',
        quoting=csv.QUOTE_MINIMAL)

    writer.writerow(header)

    for data in export_datas:
        writer.writerow(data)
    return response