#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse
from django.http import QueryDict


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    # 编辑或删除的时候，有个pk的参数，所以使用args,kwargs
    # re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    # {% memory_url request 'rbac:menu_edit' pk=row.id %}
    basic_url = reverse(name, args=args, kwargs=kwargs)

    # 当前URL中无参数,即没有?mid=2
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  # 获取路径后的参数mid=2&age=99
    # 不能直接使用字符串的拼接
    # 因为/menu/add/_filter=mid=2&age=27这样就是_filter=mid=2，而不是_filter=""mid=2&age=27,含义就变了
    # 所以这里使用query_dict进行打包，然后给key赋值
    # query_dict.urlencode()以url的编码格式返回数据字符串
    # 在HttpRequest对象中，GET和POST属性都是一个django.http.QueryDict的实例
    # QueryDict 实现了Python字典数据类型的所有标准方法，因为它是字典的子类。
    return "%s?%s" % (basic_url, query_dict.urlencode())


def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成URL
        http://127.0.0.1:8001/rbac/menu/add/?_filter=mid%3D2
        1. 在url中讲原来搜索条件，如filter后的值
        2. reverse生成原来的URL，如：/menu/list/
        3. /menu/list/?mid%3D2

    示例：
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = "%s?%s" % (url, origin_params,)

    return url
