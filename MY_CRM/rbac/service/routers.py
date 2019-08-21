#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import URLResolver, URLPattern
from django.urls.resolvers import RegexPattern, RoutePattern


def check_url_exclude(url):
    """
    排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归的去获取URL,只获取有name的url
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发，讲路由添加到url_ordered_dict
            # 没有设置name别名，就跳过

            if not item.name:
                continue

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            # 下面是获取配置的url
            pattern = ""
            if isinstance(item.pattern, URLPattern) or isinstance(item.pattern, RoutePattern):
                pattern = item.pattern._route
            elif isinstance(item.pattern, RegexPattern):
                pattern = item.pattern._regex
            url = pre_url + pattern  # /rbac/user/edit/(?P<pk>\d+)/
            # 起始符和终止符去掉
            url = url.replace('^', '').replace('$', '')

            if check_url_exclude(url):
                continue

            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):  # 路由分发，递归操作

            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:

                    namespace = None
            #         pattern是获取配置的url,
            url = ""
            if isinstance(item.pattern, URLPattern) or isinstance(item.pattern, RoutePattern):
                url = item.pattern._route
            elif isinstance(item.pattern, RegexPattern):
                url = item.pattern._regex

            recursion_urls(namespace, pre_url + url, item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
   获取项目中所有的URL（必须有name别名）
   :return:
   """
    from django.utils.module_loading import import_string
    from django.conf import settings
    md = import_string(settings.ROOT_URLCONF)  # from luff.. import urls
    # <URLResolver <URLPattern list> (admin:admin) 'admin/'>
    # <URLResolver <module 'web.urls' from '**permission\\web\\urls.py'> (web:web) '^'>
    # <URLResolver <module 'rbac.urls' from '**permission\\rbac\\urls.py'> (rbac:rbac) 'rbac/'>
    # <URLPattern '^user/list/$' [name='user_list']>
    # urlpatterns = [
    #     path('admin/', admin.site.urls),
    #     re_path(r'^', include('web.urls', namespace="web")),
    #     re_path(r'rbac/', include('rbac.urls', namespace="rbac")),
    #     re_path(r'^user/list/$', user.user_list, name='user_list'),
    # ]
    # for item in md.urlpatterns:
    #     print(item)
    url_ordered_dict = OrderedDict()
    """
    {
    "rbac:menu_list":{name:'rbac:menu_list',url:"menu/list/"}
    }
    """
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    print("url_ordered_dict----------------------------",url_ordered_dict)
    return url_ordered_dict
# OrderedDict([('web:customer_list', {'name': 'web:customer_list', 'url': '/customer/list/'}),
# ('web:customer_add', {'name': 'web:customer_add', 'url': '/customer/add/'}),
# ('web:customer_edit', {'name': 'web:customer_edit', 'url': '/customer/edit/(?P<cid>\\d+)/'}),
# ('web:customer_del', {'name': 'web:customer_del', 'url': '/customer/del/(?P<cid>\\d+)/'}),
# ('web:customer_import', {'name': 'web:customer_import', 'url': '/customer/import/'}),
# ('web:customer_tpl', {'name': 'web:customer_tpl', 'url': '/customer/tpl/'}),
# ('web:payment_list', {'name': 'web:payment_list', 'url': '/payment/list/'}),
# ('web:payment_add', {'name': 'web:payment_add', 'url': '/payment/add/'}),
# ('web:payment_edit', {'name': 'web:payment_edit', 'url': '/payment/edit/(?P<pid>\\d+)/'}),
# ('web:payment_del', {'name': 'web:payment_del', 'url': '/payment/del/(?P<pid>\\d+)/'}),
# ('rbac:role_list', {'name': 'rbac:role_list', 'url': '/rbac/role/list/'}),
# ('rbac:role_add', {'name': 'rbac:role_add', 'url': '/rbac/role/add/'}),
# ('rbac:role_edit', {'name': 'rbac:role_edit', 'url': '/rbac/role/edit/(?P<pk>\\d+)/'}),
# ('rbac:role_del', {'name': 'rbac:role_del', 'url': '/rbac/role/del/(?P<pk>\\d+)/'}),
# ('rbac:user_list', {'name': 'rbac:user_list', 'url': '/rbac/user/list/'}),
# ('rbac:user_add', {'name': 'rbac:user_add', 'url': '/rbac/user/add/'}),
# ('rbac:user_edit', {'name': 'rbac:user_edit', 'url': '/rbac/user/edit/(?P<pk>\\d+)/'}),
# ('rbac:user_del', {'name': 'rbac:user_del', 'url': '/rbac/user/del/(?P<pk>\\d+)/'}),
# ('rbac:user_reset_pwd', {'name': 'rbac:user_reset_pwd', 'url': '/rbac/user/reset/password/(?P<pk>\\d+)/'}),
# ('rbac:menu_list', {'name': 'rbac:menu_list', 'url': '/rbac/menu/list/'}),
# ('rbac:menu_add', {'name': 'rbac:menu_add', 'url': '/rbac/menu/add/'}),
# ('rbac:menu_edit', {'name': 'rbac:menu_edit', 'url': '/rbac/menu/edit/(?P<pk>\\d+)/'}),
# ('rbac:menu_del', {'name': 'rbac:menu_del', 'url': '/rbac/menu/del/(?P<pk>\\d+)/'}),
# ('rbac:second_menu_add', {'name': 'rbac:second_menu_add', 'url': '/rbac/second/menu/add/(?P<menu_id>\\d+)'}),
# ('rbac:second_menu_edit', {'name': 'rbac:second_menu_edit', 'url': '/rbac/second/menu/edit/(?P<pk>\\d+)/'}),
# ('rbac:second_menu_del', {'name': 'rbac:second_menu_del', 'url': '/rbac/second/menu/del/(?P<pk>\\d+)/'}),
# ('rbac:permission_add', {'name': 'rbac:permission_add', 'url': '/rbac/permission/add/(?P<second_menu_id>\\d+)/'}),
# ('rbac:permission_edit', {'name': 'rbac:permission_edit', 'url': '/rbac/permission/edit/(?P<pk>\\d+)/'}),
# ('rbac:permission_del', {'name': 'rbac:permission_del', 'url': '/rbac/permission/del/(?P<pk>\\d+)/'}),
# ('user_list', {'name': 'user_list', 'url': '/user/list/'})])