#!/usr/bin/env python
# -*- coding:utf-8 -*-
import functools
from types import FunctionType
from django.conf.urls import url
from django.db.models import Q
from django import forms
from django.urls import reverse
from django.http import QueryDict
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from stark.utils.pagination import Pagination
from django.db.models import ForeignKey, ManyToManyField
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
    def __init__(self, field, db_condition=None, text_func=None, value_func=None,  is_multi=False):
        """
        :param field: 组合搜索关联的字段
        :param db_condition: 数据库关联查询时的条件
        :param text_func: 此函数用于显示组合搜索按钮页面文本
        :param value_func: 此函数用于显示组合搜索按钮值
        """
        self.field = field
        if not db_condition:
            db_condition = {}
        self.db_condition = db_condition
        self.text_func = text_func
        self.value_func = value_func
        self.is_multi = is_multi
        self.is_choice = False

    def get_db_condition(self, request, *args, **kwargs):
        return self.db_condition

    def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
        """
        根据字段去获取数据库关联的数据
        :return:
        """
        # 根据gender或depart字符串，去自己对应的Model类中找到 字段对象
        field_object = model_class._meta.get_field(self.field)
        title = field_object.verbose_name
        # 获取关联数据
        if isinstance(field_object, ForeignKey) or isinstance(field_object, ManyToManyField):
            # FK和M2M,应该去获取其关联表中的数据： QuerySet
            db_condition = self.get_db_condition(request, *args, **kwargs)
            print(self.field, field_object.remote_field.model.objects.filter(**db_condition))
            #     depart <QuerySet [<Depart: dep1>]>
            return SearchGroupRow(title, field_object.remote_field.model.objects.filter(**db_condition), self, request.GET)
        else:
            # 获取choice中的数据
            print(self.field, field_object.choices)
            #             gender ((1, '男'), (2, '女'))
            # 获取choice中的数据：元组
            self.is_choice = True
            return SearchGroupRow(title, field_object.choices, self,request.GET)
    def get_value(self, field_object):
        if self.value_func:
            return self.value_func(field_object)

        if self.is_choice:
            return field_object[0]

        return field_object.pk
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

        return str(field_object)

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

class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



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
        """
        添加，编辑，删除成功后，返回首页
        带有原搜索条件，解包被打包的内容
        :return:
        """

        name = "%s:%s" % (self.site.namespace, self.get_list_url_name,)
        base_url = reverse(name)
        param = self.request.GET.get('_filter')
        if not param:
            return base_url
        return "%s?%s" % (base_url, param,)

    def reverse_add_url(self):
        """
        带有原搜索条件，把原搜索条件打包
        :return:
        """
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

    def reverse_change_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的编辑URL
        :param args:
        :param kwargs:
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_change_url_name,)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def reverse_delete_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的删除URL
        :param args:
        :param kwargs:
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_delete_url_name,)
        base_url = reverse(name, args=args, kwargs=kwargs)
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
        return mark_safe('<a href="%s">编辑</a>' % self.reverse_change_url(pk=obj.pk))

    def display_del(self, obj=None, is_header=None):
        if is_header:
            return "删除"
        name = "%s:%s" % (self.site.namespace, self.get_delete_url_name,)
        return mark_safe('<a href="%s">删除</a>' % self.reverse_delete_url(pk=obj.pk))

    order_list = []

    def get_order_list(self):
        return self.order_list or ['-id', ]

    search_list = []

    def get_search_list(self):
        return self.search_list

    def display_checkbox(self, obj=None, is_header=None):
        """
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "选择"
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' % obj.pk)
    action_list = []

    def get_action_list(self):
        return self.action_list
    def action_multi_delete(self, request, *args, **kwargs):
        """
        批量删除（如果想要定制执行成功后的返回值，那么就为action函数设置返回值即可。）
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        # return redirect("http://www.baidu.com")

    action_multi_delete.text = "批量删除"
    search_group = []

    def get_search_group(self):
        return self.search_group
    def get_search_group_condition(self, request):
        """
        获取组合搜索的条件
        :param request:
        :return:
        """
        condition = {}
        # ?depart=1&gender=2&page=123&q=999
        for option in self.get_search_group():
            values_list = request.GET.getlist(option.field)  # tags=[1,2]
            if not values_list:
                continue
            condition['%s__in' % option.field] = values_list
        return condition
    def changelist_view(self, request, *args, **kwargs):
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
        # ########## 1. 处理Action ##########
        action_list = self.get_action_list()
        action_dict = {func.__name__: func.text for func in action_list}  # {'multi_delete':'批量删除','multi_init':'批量初始化'}
        if request.method == 'POST':
            # 批量操作，执行对应的函数
            action_func_name = request.POST.get('action')
            if action_func_name and action_func_name in action_dict:
                # 如果该函数想批量操作完成后，跳转，可以给函数写返回值
                action_response = getattr(self, action_func_name)(request, *args, **kwargs)
                if action_response:
                    # return redirect("http://www.baidu.com")
                    return action_response

        search_list = self.get_search_list()
        search_value = request.GET.get('q', '')
        conn = Q()
        conn.connector = 'OR'
        if search_value:

            for item in search_list:
                conn.children.append((item, search_value))
        # ########## 1. 获取排序 ##########
        order_list = self.get_order_list()

        # 获取组合的条件
        search_group_condition = self.get_search_group_condition(request)
        queryset = self.model_class.objects.filter(conn).filter(**search_group_condition).order_by(*order_list)

        # ########## 2. 处理分页 ##########
        all_count = queryset.count()

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

        data_list = queryset[pager.start:pager.end]

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

        # ########## 7. 组合搜索 #########
        search_group_row_list = []
        search_group = self.get_search_group()  # ['gender', 'depart']
        for option_object in search_group:
            row = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            search_group_row_list.append(row)

        return render(
            request,
            'stark/changelist.html',
            {
                'data_list': data_list,
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'search_list': search_list,
                'search_value': search_value,
                'action_dict': action_dict,
                'add_btn': add_btn,
                'search_group_row_list': search_group_row_list
            }
        )
    # 默认添加或编辑都是展示所有字段，可以自定义model_form_class，设置展示哪些字段
    model_form_class = None

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm
    def save(self, form, is_update=False):
        """
        在使用ModelForm保存数据之前预留的钩子方法
        :param form:
        :param is_update:
        :return:
        """
        form.save()

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """
        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'stark/change.html', {'form': form})
        form = model_form_class(data=request.POST)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def change_view(self, request, pk):
        """
        编辑页面
        :param request:
        :param pk:
        :return:
        """
        current_change_object = self.model_class.objects.filter(pk=pk).first()
        if not current_change_object:
            return HttpResponse('要修改的数据不存在，请重新选择！')

        model_form_class = self.get_model_form_class()
        if request.method == 'GET':
            form = model_form_class(instance=current_change_object)
            return render(request, 'stark/change.html', {'form': form})
        form = model_form_class(data=request.POST, instance=current_change_object)
        if form.is_valid():
            self.save(form, is_update=False)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """
        origin_list_url = self.reverse_list_url()
        if request.method == 'GET':
            return render(request, 'stark/delete.html', {'cancel': origin_list_url})

        self.model_class.objects.filter(pk=pk).delete()
        return redirect(origin_list_url)

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
            url(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
            url(r'^delete/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
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
