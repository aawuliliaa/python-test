#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from permission import settings


class CheckPermissionMiddleware(MiddlewareMixin):
    """
    定义用户访问权限的中间件
    对用户可访问的菜单进行校验
    """
    def process_request(self, request):
        """
        1. 获取当前用户请求的URL
        2. 如果是白名单中的URL放行
        3. 不在白名单中，获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        4. 如果用户没有登陆，session中是没有该key的，提示用户登录，登录后会把能够访问的菜单信息存入url中
        5. 权限信息匹配，在session中有当前访问的URL，放行，不在，拒绝访问
        中间件返回None,是能够继续运行views.py的
        {}.get(key)，key不存在时，不会报错。
        :param request:
        :return:
        """
        white_list = settings.WHITE_LIST
        current_path = request.path_info  # 访问[INFO] "GET /customer/list/?wewe，request.path_info=/customer/list/
        for white_url_li in white_list:
            # 如果是白名单中的url，就放行
            if re.match(white_url_li, current_path):
                return None
        session_permission_url = request.session.get(settings.SESSION_PERMISSION_URL)
        # 如果用户没有登陆，session中是没有该key的，提示用户登录，登录后会把能够访问的菜单信息存入url中
        if session_permission_url is None:
            return HttpResponse("session中还没有url信息，请登录之后再访问！")
        # 循环用户可访问的菜单列表，如果当前路径在可访问的菜单列表中，就放行，否则就返回拒绝访问
        # print("---------------------session_permission_url_list", session_permission_url_list)
        # [{'id': 1, 'url': '/customer/list/', 'pid': None}, {'id': 2, 'url': '/customer/add/', 'pid': 1},
        # {'id': 7, 'url': '/payment/list/', 'pid': None}, {'id': 8, 'url': '/payment/add/', 'pid': 7}]
        flag = False
        # 用于路径导航
        url_record = [{'title': "首页", "url": "#"}]
        # [{'title': '首页', 'url': '#'},
        # {'title': '客户列表', 'url': '/customer/list/'},
        # {'title': '添加客户', 'url': '/customer/add/', 'class': 'active'}]
        for permission_item in session_permission_url.values():
            if re.match(permission_item["url"], current_path):
                flag = True
                request.current_selected_permission = permission_item['pid'] or permission_item['id']
                if not permission_item["pid"]:
                    url_record.append({'title': permission_item['title'],
                                       'url': permission_item["url"],
                                       'class': 'active'})
                else:
                    url_record.extend([{'title': permission_item['p_title'],
                                        'url': permission_item["p_url"]},
                                       {'title': permission_item['title'],
                                        'url': permission_item["url"],
                                        'class': 'active'}])
                request.breadcrumb = url_record

        if flag is False:
            return HttpResponse("没有访问该菜单的权限")