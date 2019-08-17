#!/usr/bin/env python
# -*- coding:utf-8 -*-
import functools
from types import FunctionType
from django.conf.urls import url

from django import forms
from django.urls import reverse
from django.http import QueryDict
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render
from stark.utils.pagination import Pagination

def get_choice_text(title, field):
    """
    对于Stark组件中定义列时，choice如果想要显示中文信息，调用此方法即可。
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :return:
    """

    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        method = "get_%s_display" % field
        return getattr(obj, method)()

    return inner


class StarkHandler(object):
    list_display = []
    per_page_count = 10
    def get_list_display(self):
        """
        获取页面上应该显示的列，预留的自定义扩展，例如：以后根据用户的不同显示不同的列
        :return:
        """
        value = []
        value.extend(self.list_display)
        return value

    def __init__(self, site, model_class, prev):
        self.site = site
        self.model_class = model_class
        self.prev = prev
        self.request = None
    has_add_btn = True

    def get_add_btn(self):
        if self.has_add_btn:
            return "<a class='btn btn-primary' href='%s'>添加</a>" % self.reverse_add_url()
        return None

    def reverse_list_url(self):
        name = "%s:%s" % (self.site.namespace, self.get_list_url_name,)
        base_url = reverse(name)
        param = self.request.GET.get('_filter')
        if not param:
            return base_url
        return "%s?%s" % (base_url, param,)

    def reverse_add_url(self):
        name = "%s:%s" % (self.site.namespace, self.get_add_url_name,)
        base_url = reverse(name)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def display_edit(self, obj=None, is_header=None):
        """
        自定义页面显示的列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "编辑"
        name = "%s:%s" % (self.site.namespace, self.get_change_url_name,)
        return mark_safe('<a href="%s">编辑</a>' % reverse(name, args=(obj.pk,)))

    def display_del(self, obj=None, is_header=None):
        if is_header:
            return "删除"
        name = "%s:%s" % (self.site.namespace, self.get_delete_url_name,)
        return mark_safe('<a href="%s">删除</a>' % reverse(name, args=(obj.pk,)))
    def changelist_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        # 访问http://127.0.0.1:8000/stark/app01/depart/list/； self.model_class = app01.models.Depart
        # 访问http://127.0.0.1:8000/stark/app01/userinfo/list/； self.model_class = app01.models.UserInfo
        # 访问http://127.0.0.1:8000/stark/app02/role/list/； self.model_class = app02.models.Role
        # 访问http://127.0.0.1:8000/stark/app02/host/list/； self.model_class =app02.models.Host
        # self.models_class

        # ########## 1. 处理分页 ##########
        all_count = self.model_class.objects.all().count()
        # 默认是不可以被修改的
        query_params = request.GET.copy()
        # 该项设置为True，就可以修改了
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )

        data_list = self.model_class.objects.all()[pager.start:pager.end]

        # ########## 2. 处理表格 ##########
        list_display = self.get_list_display()
        # 1. 处理表格的表头
        header_list = []
        if list_display:
            for key_or_func in list_display:
                if isinstance(key_or_func, FunctionType):
                    verbose_name = key_or_func(self, obj=None, is_header=True)
                else:
                    verbose_name = self.model_class._meta.get_field(key_or_func).verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)

        # 2. 处理表的内容
        # data_list = self.model_class.objects.all()

        body_list = []
        for row in data_list:
            tr_list = []
            if list_display:
                for key_or_func in list_display:
                    # obj = Foo()
                    # # obj.func('wupeiqi') # 方法
                    # print(obj.func)  # <bound method Foo.func of <__main__.Foo object at 0x00000184BC63D390>>
                    # 不需要手动传递self
                    # 如果是函数
                    # # obj = Foo()
                    # # Foo.func(obj, 'vita') # 函数
                    # print(Foo.func)  # <function Foo.func at 0x00000184BE473950>
                    # 需要手动传递self
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, is_header=False))
                    else:
                        tr_list.append(getattr(row, key_or_func))  # obj.gender
            else:
                tr_list.append(row)
            body_list.append(tr_list)

        # ##########3. 添加按钮 #########
        add_btn = self.get_add_btn()
        return render(
            request,
            'stark/changelist.html',
            {
                'data_list': data_list,
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'add_btn': add_btn
            }
        )

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """
        # self.models_class
        return HttpResponse('添加页面')

    def change_view(self, request, pk):
        """
        编辑页面
        :param request:
        :param pk:
        :return:
        """
        # self.models_class
        return HttpResponse('编辑页面')

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """
        # self.models_class
        return HttpResponse('删除页面')

    def get_url_name(self, param):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param,)
        return '%s_%s_%s' % (app_label, model_name, param,)

    @property
    def get_list_url_name(self):
        """
        获取列表页面URL的name
        :return:
        """
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        """
        获取添加页面URL的name
        :return:
        """
        return self.get_url_name('add')

    @property
    def get_change_url_name(self):
        """
        获取修改页面URL的name
        :return:
        """
        return self.get_url_name('change')

    @property
    def get_delete_url_name(self):
        """
        获取删除页面URL的name
        :return:
        """
        return self.get_url_name('delete')

    def wrapper(self, func):
        # 保留原函数的元信息，建议都加上
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner
    def get_urls(self):
        patterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            url(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            url(r'^change/(\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
            url(r'^delete/(\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    def extra_urls(self):
        return []



class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        """

        :param model_class: 是models中的数据库表对应的类。 models.UserInfo
        :param handler_class: 处理请求的视图函数所在的类
        :param prev: 生成URL的前缀
        :return:
        """
        """
        self._registry = [
            {'prev':None, 'model_class':models.Depart,'handler': DepartHandler(models.Depart,prev)对象中有一个model_class=models.Depart   },
            {'prev':'private', 'model_class':models.UserInfo,'handler':  StarkHandler(models.UserInfo,prev)对象中有一个model_class=models.UserInfo   }
            {'prev':None, 'model_class':models.Host,'handler':  HostHandler(models.Host,prev)对象中有一个model_class=models.Host   }
        ]
        """
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append({'model_class': model_class, 'handler': handler_class(self, model_class, prev), 'prev': prev})

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            # 方式二：
            #     include函数主要返回有三个元素的元组。
            #     from django.conf.urls import url,include
            #     from app01 import urls
            #     urlpatterns = [
            #         url(r'^web/', (urls, app_name, namespace)), # 第一个参数是urls文件对象，通过此对象可以获取urls.patterns获取分发的路由。
            #     ]
            if prev:
                patterns.append(url(r'^%s/%s/%s/' % (app_label, model_name, prev,), (handler.get_urls(), None, None)))
            else:
                patterns.append(url(r'%s/%s/' % (app_label, model_name,), (handler.get_urls(), None, None)))

        return patterns

    @property
    def urls(self):
        # 这里是返回一个元组，
        # 方式三：
        #     urlpatterns = [
        #         url(r'^web/', ([
        #             url(r'^index/', views.index),
        #             url(r'^home/', views.home),
        #         ], app_name, namespace)), # 第一个参数是urls文件对象，通过此对象可以获取urls.patterns获取分发的路由。
        #     ]

        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
