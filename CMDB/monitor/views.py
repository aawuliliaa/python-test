from django.urls import reverse

import hashlib
from web.utils import *
from web.page import *
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import pymysql
from monitor.models import Template, MonitorItem
from monitor.form import *
from monitor.utils import get_table_name
#链接
conn=pymysql.connect(host='10.0.0.61',
                     user='root',
                     password='123',
                     database='cmdb',
                     charset='utf8')
#游标
#cursor=conn.cursor() #执行完毕返回的结果集默认以元组显示
cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)

class TemplateView(View):
    """
    模板信息
    """

    def get(self, request, *args, **kwargs):
        # # 批量创建测试数据
        # list = []
        # for i in range(101,201):
        #     item = Environment(name="env_%s" % i, abs_name="env_%s" % i,
        #     note="env_%s" % i)
        #     list.append(item)
        #
        # Environment.objects.bulk_create(list)
        left_label_dic = get_label(request)
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()

        data_obj_set = Template.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("name"))
        return render(request, 'monitor/template.html', locals())


class AddTemplate(View):
    """
    添加模板信息
    """
    def get(self, request):
        left_label_dic = get_label(request)
        form = TemplateForm()
        return render(request, 'monitor/add_edit_template.html', locals())

    def post(self, request):
        left_label_dic = get_label(request)
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("monitor:template"))
        return render(request, 'monitor/add_edit_template.html', locals())


class DelTemplate(View):
    """
    删除模板信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        Template.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("monitor:template"))


class EditTemplate(View):
    """
    编辑功能就使用了modelform自带的逻辑，如果想自定义逻辑，可能还是使用form把
    """

    edit_template = None

    def get(self, request, **kwargs):
        left_label_dic = get_label(request)
        self.edit_template = Template.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = TemplateForm(instance=self.edit_template)  # 接收实例对象
        return render(request, "monitor/add_edit_template.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        name = request.POST.get("name")
        template_set = Template.objects.filter(name=name)
        template_set.update(note=request.POST.get("note"))
        template_obj = template_set.first()

        notifier_role_list = request.POST.getlist("notifier_role")
        host_list = request.POST.getlist("host")
        monitor_item_list = request.POST.getlist("monitor_item")
        template_obj.notifier_role.set(notifier_role_list)
        template_obj.host.set(host_list)
        template_obj.monitor_item.set(monitor_item_list)

        return redirect(reverse("monitor:template"))


class MonitorItemView(View):
    """
    模板信息
    """

    def get(self, request, *args, **kwargs):
        # # 批量创建测试数据
        # list = []
        # for i in range(101,201):
        #     item = Environment(name="env_%s" % i, abs_name="env_%s" % i,
        #     note="env_%s" % i)
        #     list.append(item)
        #
        # Environment.objects.bulk_create(list)
        left_label_dic = get_label(request)
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()

        data_obj_set = MonitorItem.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("name"))
        return render(request, 'monitor/monitor_item.html', locals())


class AddMonitorItem(View):
    """
    添加模板信息
    """
    def get(self, request):
        left_label_dic = get_label(request)
        form = MonitorItemForm()
        return render(request, 'monitor/add_edit_monitor_item.html', locals())

    def post(self, request):
        left_label_dic = get_label(request)
        form = MonitorItemForm(request.POST)
        name = request.POST.get("name")
        if form.is_valid():
            table_name = get_table_name(name)

            sql_createTb = """CREATE TABLE  IF NOT EXISTS %s (
                             id INT NOT NULL AUTO_INCREMENT,
                             get_data_time  datetime(6) NOT NULL,
                             ip  varchar(255) NOT NULL,
                             data  varchar(255) NOT NULL,
                             warn  varchar(255) DEFAULT NULL,
                             PRIMARY KEY(id))
                             """ % table_name
            # 防止sql注入，，使用execute来进行字符串拼接
            # 这里不能使用execute拼接字符串，会添加一个'字符，怎样都报语法错误，所以就使用默认的字符串拼接了
            res = cursor.execute(sql_createTb)

            form.save()
            return redirect(reverse("monitor:monitor_item"))
        return render(request, 'monitor/add_edit_monitor_item.html', locals())


class DelMonitorItem(View):
    """
    删除模板信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        monitor_item_set = MonitorItem.objects.filter(id=kwargs.get("pk"))
        name = monitor_item_set.first().name
        table_name = get_table_name(name)
        # 删除该项对应的表
        drop_table_sql = "drop table if exists %s" % table_name
        cursor.execute(drop_table_sql)  # 如果表存在则删除
        # 删除该条监控项
        monitor_item_set.delete()
        return redirect(reverse("monitor:monitor_item"))


class EditMonitorItem(View):
    """
    编辑功能就使用了modelform自带的逻辑，如果想自定义逻辑，可能还是使用form把
    """

    edit_monitor_item = None

    def get(self, request, **kwargs):
        left_label_dic = get_label(request)
        self.edit_monitor_item = MonitorItem.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = MonitorItemForm(instance=self.edit_monitor_item)  # 接收实例对象
        return render(request, "monitor/add_edit_monitor_item.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        name = request.POST.get("name")
        monitor_item_set = MonitorItem.objects.filter(name=name)
        monitor_item_set.update(note=request.POST.get("note"),
                                monitor_script=request.POST.get("monitor_script"),
                                warn_expression=request.POST.get("warn_expression"),
                                time_interval=request.POST.get("time_interval"),
                                warn_type=request.POST.get("warn_type"))

        return redirect(reverse("monitor:monitor_item"))