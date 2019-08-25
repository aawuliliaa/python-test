#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import functools
from django.db.models import ForeignKey, ManyToManyField
from types import FunctionType
from django.utils.safestring import mark_safe
from django.urls import re_path, reverse
from django.shortcuts import render, redirect, HttpResponse
from django.http import QueryDict
from stark.service.StarkModelForm import StarkModelForm
from django.db.models import Q
from stark.utils.pagination import Pagination
"""
self.model_class._meta.get_field(field).verbose_name
field_object = model_class._meta.get_field(self.field)
app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
"""


class SearchGroupRow(object):
    def __init__(self, title, queryset_or_tuple, option, query_dict):
        """

       :param title: 组合搜索的列名称
       :param queryset_or_tuple: 组合搜索关联获取到的数据
       :param option: 配置
       :param query_dict: request.GET
       """
        self.title = title
        self.queryset_or_tuple = queryset_or_tuple
        self.option = option
        self.query_dict = query_dict

    def __iter__(self):
        yield '<div class="whole">'
        yield self.title
        yield '</div>'
        yield '<div class="others">'
        total_query_dict = self.query_dict.copy()
        total_query_dict._mutable = True

        origin_value_list = self.query_dict.getlist(self.option.field)
        if not origin_value_list:
            yield "<a class='active' href='?%s'>全部</a>" % total_query_dict.urlencode()
        else:
            total_query_dict.pop(self.option.field)
            yield "<a href='?%s'>全部</a>" % total_query_dict.urlencode()

        for item in self.queryset_or_tuple:
            text = self.option.get_text(item)
            value = str(self.option.get_value(item))
            query_dict = self.query_dict.copy()
            query_dict._mutable = True

            if not self.option.is_multi:
                query_dict[self.option.field] = value
                if value in origin_value_list:
                    query_dict.pop(self.option.field)
                    yield "<a class='active' href='?%s'>%s</a>" % (query_dict.urlencode(), text)
                else:
                    yield "<a href='?%s'>%s</a>" % (query_dict.urlencode(), text)
            else:
                # {'gender':['1','2']}
                multi_value_list = query_dict.getlist(self.option.field)
                if value in multi_value_list:
                    multi_value_list.remove(value)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield "<a class='active' href='?%s'>%s</a>" % (query_dict.urlencode(), text)
                else:
                    multi_value_list.append(value)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield "<a href='?%s'>%s</a>" % (query_dict.urlencode(), text)

        yield '</div>'


class Option(object):
    def __init__(self, field, is_multi=False, db_condition=None, text_func=None, value_func=None):
        """
        :param field: 组合搜索关联的字段
        :param is_multi: 是否支持多选
        :param db_condition: 数据库关联查询时的条件
        :param text_func: 此函数用于显示组合搜索按钮页面文本
        :param value_func: 此函数用于显示组合搜索按钮值
        """
        self.field = field
        self.is_multi = is_multi
        if not db_condition:
            db_condition = {}
        self.db_condition = db_condition
        self.text_func = text_func
        self.value_func = value_func
        self.is_choice = False

    def get_db_condition(self, request, *args, **kwargs):
        return self.db_condition

    def get_text(self, field_object):
        """
        获取文本函数
        :param field_object:
        :return:
        """
        if self.text_func:
            return self.text_func(field_object)

        if self.is_choice:
            return field_object[1]
        # 如果是对象，就返回对象，这里的值是models.py中的类 __str__的返回值
        return str(field_object)

    def get_value(self, field_object):
        """
        获取值的函数
        :param field_object:
        :return:
        """
        if self.value_func:
            return self.value_func(field_object)

        if self.is_choice:
            return field_object[0]

        return field_object.pk

    def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
        """
        根据字段去获取数据库中关联的数据
        :param model_class:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        field_object = model_class._meta.get_field(self.field)
        title = field_object.verbose_name
        # 获取关联数据
        if isinstance(field_object, ForeignKey) or isinstance(field_object, ManyToManyField):
            # FK和M2M,应该去获取其关联表中的数据： QuerySet
            db_condition = self.get_db_condition(request, *args, **kwargs)
            return SearchGroupRow(title, field_object.remote_field.model.objects.filter(**db_condition), self,
                                  request.GET)
        else:
            # 获取choice中的数据：元组
            self.is_choice = True
            return SearchGroupRow(title, field_object.choices, self, request.GET)





class StarkHandler(object):
    add_template = None
    edit_template = None
    del_template = None
    list_template = None
    model_form_class = None
    # 列表页面展示的列
    # list_display = [StarkHandler.display_checkbox, 'name', 'qq', get_m2m_text('咨询课程', 'course'), display_record,
    #               get_choice_text('状态', 'status')]
    list_display = []
    has_add_btn = True
    # 搜索按钮-----搜索条件
    # search_list = ['customer__name', 'qq', 'mobile', ]
    search_list = []
    # 排序的规则
    # order_list = ['-id','confirm_status']
    order_list = []
    # 每页的数据量
    per_page_count = 10
    # 批量事件列表
    action_list = []
    # 组合搜索
    # search_group = [
    #         Option('class_list', text_func=lambda x: '%s-%s' % (x.school.title, str(x)))
    #     ]
    #   search_group = [
    #         Option('school',is_multi=True),
    #         Option('course'),
    #     ]
    search_group = []

    def __init__(self, site, model_class, prev):
        self.site = site
        self.model_class = model_class
        self.prev = prev
        self.request = None

    def get_url_name(self, param):
        """
        返回url别名
        :param param:
        :return:
        """
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return "%s_%s_%s_%s" % (app_label, model_name, self.prev, param)
        else:
            return "%s_%s_%s" % (app_label, model_name, param)

    @property
    def get_list_url_name(self):
        """
        单独设置为一个函数，是为了可扩展性，在自己定义类的时候，可重写该函数
        获取列表页面的URL的name
        :return:
        """
        return self.get_url_name("list")

    @property
    def get_add_url_name(self):
        """
        单独设置为一个函数，是为了可扩展性，在自己定义类的时候，可重写该函数
        返回添加功能的URL的name
        :return:
        """
        return self.get_url_name("add")

    @property
    def get_edit_url_name(self):
        """
        单独设置为一个函数，是为了可扩展性，在自己定义类的时候，可重写该函数
        获取编辑页面URL的name
        :return:
        """
        return self.get_url_name("edit")

    @property
    def get_del_url_name(self):
        """
        单独设置为一个函数，是为了可扩展性，在自己定义类的时候，可重写该函数
        获取删除页面的URL的name
        :return:
        """
        return self.get_url_name("del")

    def reverse_common_url(self, name, *args, **kwargs):
        """
        根据url的name反向生成URL,主要用于增加，编辑，删除按钮的a标签的href
        同时具有URL的记忆功能，保留原参数，这样添加，编辑，删除操作完成后，返回原页面，并且原页面的样式不变
        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        name = "%s:%s" % (self.site.namespace, name)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            reverse_url = base_url
        else:
            new_query_dic = QueryDict(mutable=True)
            new_query_dic["_filter"] = self.request.GET.urlencode()
            reverse_url = "%s?%s" % (base_url, new_query_dic.urlencode())
        return reverse_url

    def reverse_add_url(self, *args, **kwargs):
        """
        根据url的name反向生成添加按钮的URL
        同时具有URL的记忆功能，保留原参数，这样添加，编辑，删除操作完成后，返回原页面，并且原页面的样式不变

        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_common_url(self.get_add_url_name, *args, **kwargs)

    def reverse_edit_url(self, *args, **kwargs):
        """
        根据url的name反向生成编辑按钮的URL
        同时具有URL的记忆功能，保留原参数，这样添加，编辑，删除操作完成后，返回原页面，并且原页面的样式不变

        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_common_url(self.get_edit_url_name, *args, **kwargs)

    def reverse_del_url(self, *args, **kwargs):
        """
        根据url的name反向生成删除按钮的URL
        同时具有URL的记忆功能，保留原参数，这样添加，编辑，删除操作完成后，返回原页面，并且原页面的样式不变

        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_common_url(self.get_del_url_name, *args, **kwargs)

    def reverse_list_url(self, *args, **kwargs):
        """
        添加，编辑，删除成功后，返回列表页面
        :param args:
        :param kwargs:
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_list_url_name)
        base_url = reverse(name, *args, **kwargs)
        if self.request.GET.get("_filter"):
            return "%s?%s" % (base_url, self.request.GET.get("_filter"))
        else:
            return base_url

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        """
        定制添加和编辑的model_form
        :param is_add:
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"
        return DynamicModelForm

    def display_checkbox(self, obj=None, is_header=None, *args, **kwargs):
        """
        列出复选框
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return "选择"
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' % obj.pk)

    def display_edit(self, obj=None, is_header=None, *args, **kwargs):
        """
        编辑按钮
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "编辑"
        return mark_safe('<a href="%s">编辑</a>' % self.reverse_edit_url(pk=obj.pk))

    def display_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        删除按钮
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return "删除"
        return mark_safe('<a href="%s">删除</a>' % self.reverse_del_url(pk=obj.pk))

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        编辑和删除放在一列
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '操作'

        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_edit_url(pk=obj.pk), self.reverse_del_url(pk=obj.pk))
        return mark_safe(tpl)

    def get_add_btn(self, request, *args, **kwargs):
        """
        添加按钮
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.has_add_btn:
            return mark_safe("<a class='btn btn-primary' href='%s'>添加</a>" % self.reverse_add_url(*args, **kwargs))
        return None

    def get_list_display(self):
        """
        返回页面中展示的列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            # isinstance(key_or_func, FunctionType):，
            # type(self).display_edit_del类型才是FunctionType，是函数，类名.函数名()就是函数
            # self.display_edit_del类型是bounded.method,是方法。对象.函数名就是函数
            value.append(type(self).display_edit_del)
            return value

    def get_queryset(self, request, *args, **kwargs):
        """
        获取表中所有数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.model_class.objects.all()

    def get_search_list(self):
        """
        搜索按钮，返回搜索条件
        :return:
        """
        return self.search_list

    def get_order_list(self):
        """
        排序规则
        :return:
        """
        return self.order_list or ['-id', ]

    def get_action_list(self):
        """
        获取批量事件列表
        :return:
        """
        return self.action_list

    def action_multi_delete(self, request, *args, **kwargs):
        """
        批量删除
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    action_multi_delete.text = "批量删除"

    def get_search_group(self):
        return self.search_group

    def get_search_group_condition(self, request):
        """
        获取组合搜索的条件
        :param request:
        :return:
        """
        condition = {}
        for option in self.get_search_group():
            if option.is_multi:
                value_list = request.GET.getlist(option.field)  # tags=[1,2]
                if not value_list:
                    continue
                condition["%s_in" % option.field] = value_list
            else:
                value = request.GET.get(option.field)
                if not value:
                    continue
                condition[option.field] = value
        return condition

    def list_view(self, request, *args, **kwargs):
        """
        列出数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.处理Action
        action_list = self.get_action_list()
        action_dict = {func.__name__: func.text for func in action_list}
        # 用户执行批量操作
        if request.method == "POST":
            action_func_name = request.POST.get("action")
            if action_func_name in action_dict:
                action_response = getattr(self, action_func_name)(request, *args, **kwargs)
                # 如果有返回值，例如操作成功后跳转页面，函数就可以写返回值，进行页面的跳转
                # 没有返回值，还是返回当前页面
                if action_response:
                    return action_response

        # 2.搜索按钮
        search_list = self.get_search_list()
        search_value = request.GET.get("search", "")
        conn = Q()
        conn.connector = "OR"

        if search_value:
            for item in search_list:
                # 对内容进行模糊查询
                conn.children.append((item+"__icontains", search_value))
        # 3.处理排序
        order_list = self.get_order_list()
        # 4.获取组合搜索的条件
        search_group_condition = self.get_search_group_condition(request)

        # 5.获取符合条件的数据
        prev_queryset = self.get_queryset(request, *args, **kwargs)
        queryset = prev_queryset.filter(conn).filter(**search_group_condition).order_by(*order_list)

        # 6.分页
        all_count = queryset.count()

        query_params = request.GET.copy()
        query_params._mutable = True

        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )

        data_list = queryset[pager.start:pager.end]
        # 7.表格内容展示
        list_display = self.get_list_display()
        # 7.1 处理表格的表头
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

        # 7.2 处理表的内容
        body_list = []
        for row in data_list:
            tr_list = []
            if list_display:
                for key_or_func in list_display:
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, False, *args, **kwargs))
                    else:
                        tr_list.append(getattr(row, key_or_func))  # obj.gender
            else:
                tr_list.append(row)
            body_list.append(tr_list)
        # 8.添加按钮
        add_btn = self.get_add_btn(request, *args, **kwargs)
        # 9.组合搜索
        search_group_row_list = []
        search_group = self.get_search_group()  #
        for option_object in search_group:
            row = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            search_group_row_list.append(row)
        return render(
            request,
            self.list_template or 'stark/list.html',
            {
                'data_list': data_list,
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'add_btn': add_btn,
                'search_list': search_list,
                'search_value': search_value,
                'action_dict': action_dict,
                'search_group_row_list': search_group_row_list
            }
        )


    def save(self, request, form, is_update, *args, **kwargs):
        """
        在使用ModelForm保存数据之前预留的钩子方法
        :param request:
        :param form:
        :param is_update:
        :return:
        """
        form.save()

    def add_view(self, request, *args, **kwargs):
        """
        添加页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        model_form_class = self.get_model_form_class(True, request, None, *args, **kwargs)
        if request.method == "GET":
            form = model_form_class()
            return render(request, self.add_template or "stark/add_edit.html", {"form": form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            self.save(request, form, False, *args, **kwargs)
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.add_template or "stark/add_edit.html", {"form": form})

    def get_edit_object(self, request, pk, *args, **kwargs):
        """
        获取编辑数据的对象
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        return self.model_class.objects.filter(pk=pk).first()

    def edit_view(self, request, pk, *args, **kwargs):
        """
        编辑页面
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        edit_obj = self.get_edit_object(request, pk, *args, **kwargs)
        if not edit_obj:
            return HttpResponse("要修改的数据不存在，请重新选择")

        model_form_class = self.get_model_form_class(False, request, pk, *args, **kwargs)
        if request.method == "GET":
            form = model_form_class(instance=edit_obj)
            return render(request, self.edit_template or "stark/add_edit.html", {"form": form})
        form = model_form_class(data=request.POST, instance=edit_obj)
        if form.is_valid():
            self.save(request, form, True, *args, **kwargs)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.edit_template or 'stark/change.html', {'form': form})

    def del_obj(self, request, pk, *args, **kwargs):
        """
        获取删除的数据对象
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        self.model_class.objects.filter(pk=pk).delete()

    def del_view(self, request, pk, *args, **kwargs):
        """
        删除功能
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        list_url = self.reverse_list_url(*args, **kwargs)
        if request.method == "GET":
            return render(request, self.del_template or "stark/del.html", {"cancel_url": list_url})
        self.del_obj(request, pk, *args, **kwargs)
        return redirect(list_url)

    def wrapper(self, func):
        """
        主要是为了设置self.request = request
        :param func:
        :return:
        """
        @functools.wraps(func)
        # 不使用functools.wraps装饰器，添加装饰器后，func.__name__都变成了inner
        # 使用functools.wraps装饰器后，func__name__还是函数原有的名字
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)
        return inner

    def get_urls(self):
        """
        普遍使用的url
        :return:
        """
        patterns = [
            re_path(r"^list/$", self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r"^add/$", self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r"^edit/(?P<pk>\d+)/$", self.wrapper(self.edit_view), name=self.get_edit_url_name),
            re_path(r"^del/(?P<pk>\d+)/$", self.wrapper(self.del_view), name=self.get_del_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def extra_urls(self):
        """
        其余的url
        :return:
        """
        return []