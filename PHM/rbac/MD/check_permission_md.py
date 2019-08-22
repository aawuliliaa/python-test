#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class CheckPermissionMiddleware(MiddlewareMixin):
    """
    定义用户访问权限的中间件
    对用户可访问的菜单进行校验
    """
    def process_request(self, request):
        """
            1. 获取当前用户请求的URL
            2. 如果是白名单中的URL放行
            3. 不在白名单中，获取当前用户在session中保存的权限字典
            4. 如果用户没有登陆，session中是没有该key的，提示用户登录，登录后会把能够访问的菜单信息存入url中
            5.需要登陆，但是不需要进行权限校验的url
            6. 权限信息匹配，在session中有当前访问的URL，放行，不在，拒绝访问
            中间件返回None,是能够继续运行views.py的
            {}.get(key)，key不存在时，不会报错。
            :param request:
            :return:
        """
        white_list = settings.WHITE_LIST
        current_path = request.path_info  # 访问[INFO] "GET /customer/list/?wewe，request.path_info=/customer/list/
        # 1.在白名单中就放行
        for white_url_li in white_list:
            if re.match(white_url_li, current_path):
                return None
        # 2.验证session中是否有权限的key，没有，说明没有登陆，提示登录后才能访问
        session_permission_url = request.session.get(settings.SESSION_PERMISSION_URL)
        # session_permission_url = {'customer_list': {'id': 1, 'title': '客户列表',
        #     'url': '/customer/list/', 'pid': None, 'p_title': None, 'p_url': None},
        # 'customer_add': {'id': 2, 'title': '添加客户',
        #     'url': '/customer/add/', 'pid': 1, 'p_title': '客户列表', 'p_url': '/customer/list/'},
        # 'payment_list': {'id': 7, 'title': '账单列表',
        #     'url': '/payment/list/', 'pid': None, 'p_title': None, 'p_url': None},
        # 'payment_add': {'id': 8, 'title': '添加账单',
        #     'url': '/payment/add/', 'pid': 7, 'p_title': '账单列表', 'p_url': '/payment/list/'}}
        if session_permission_url is None:
            return HttpResponse("session中还没有url信息，请登录后在访问！")

        flag = False
        # 用于路径导航
        url_record = [{"title": "首页", "url": "#"}]
        # 3.需要登陆，但是不需要进行权限校验的url
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, current_path):
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None
        # 4.权限校验
        for permission_item in session_permission_url.values():
            if re.match(permission_item["url"], current_path):
                flag = True
                request.current_selected_permission = permission_item["pid"] or permission_item["id"]
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
            return HttpResponse("没有访问该菜单的权限！！！！！")

