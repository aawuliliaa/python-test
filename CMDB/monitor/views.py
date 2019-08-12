from django.urls import reverse

import hashlib
from web.utils import *
from web.page import *
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
import pymysql
from monitor.models import Template, MonitorItem
from monitor.form import *
from monitor.utils import get_table_name, get_pymysql_conn
from django.contrib.auth.decorators import login_required
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
import json
from random import randrange
from types import FunctionType

from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Page
from monitor.models import MonitorItem, Template
CurrentConfig.ONLINE_HOST = "http://10.0.0.61:8001/assets/"
# [root@m01 pyecharts-assets]# python3 -m http.server 8001&
# [1] 41184
# [root@m01 pyecharts-assets]# Serving HTTP on 0.0.0.0 port 8001 (http://0.0.0.0:8001/) ...
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates/monitor/templates/"))


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
            conn = get_pymysql_conn()
            # 游标
            # cursor=conn.cursor() #执行完毕返回的结果集默认以元组显示
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            res = cursor.execute(sql_createTb)
            # 使用完了就关闭
            cursor.close()
            conn.close()

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
        conn = get_pymysql_conn()
        # 游标
        # cursor=conn.cursor() #执行完毕返回的结果集默认以元组显示
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 删除该项对应的表
        drop_table_sql = "drop table if exists %s" % table_name
        cursor.execute(drop_table_sql)  # 如果表存在则删除
        cursor.close()
        conn.close()
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


class HostMonitor(View):
    """
    点击主机，进入监控页面
    """
    def get(self, request):
        left_label_dic = get_label(request)
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()

        data_obj_set = Host.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("name"))
        return render(request, "monitor/host_monitor.html", locals())
def bar_base() -> Bar:
    js = """
    $(function () 
        {get_bar_Data(chart_bar_id);
        setInterval(get_bar_Data, 2000);}
    );
    function get_bar_Data() {
        $.ajax({
            type: 'GET',
            url: 'http://10.0.0.61:8000/monitor/bar',
            success: function (result) 
            {chart_bar_id.setOption(result.data);}});
        }
    """

    c = (
        Bar(init_opts=opts.InitOpts(chart_id="bar_id",height="200px",width="100%"))
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values(), is_selected=False)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
        .add_js_funcs(js)

    )
    return c

def json_line_base() -> Line:
    line = (

        Line(init_opts=opts.InitOpts(height="200px", width="300px"))
    .add_xaxis(["草莓", "芒果", "葡萄", "雪梨", "西瓜", "柠檬", "车厘子"])
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
        .dump_options()
    )
    return line


class LineView(View):
    def get(self, request, *args, **kwargs):
        return MyJsonResponse(json.loads(json_line_base()))
# class BarView(View):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(json.loads(json_bar_base()))



# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


MyJsonResponse = json_response
MyJsonError = json_error


@login_required
def show_host_monitor_data(request, ip):

    from monitor.urls import urlpatterns
    from django.urls import re_path
    monitor_item_set = MonitorItem.objects.filter(template_host__host__ip=ip).distinct()
    page = Page()
    for monitor_item_obj in monitor_item_set:
        # 监控项的名称
        name = monitor_item_obj.name
        item_table_name = get_table_name(name)
        # 数据库中存的是秒，前端是定时任务中的单位是毫秒，所以要乘以1000
        time_interval = int(monitor_item_obj.time_interval)*1000
        conn = get_pymysql_conn()
        # 游标
        # cursor=conn.cursor() #执行完毕返回的结果集默认以元组显示
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 删除该项对应的表
        select_sql = "select * from %s where to_days(get_data_time) <= to_days(now()); " % item_table_name
        # select * from monitor_item_cpu_d9747e2da3 where year(get_data_time)=year(now()) and month(get_data_time)=month(now()) and day(get_data_time)=day(now())
        cursor.execute(select_sql)  # 如果表存在则删除
        todays_data_rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
        item_xaxis = []
        # {"load1":[1,2,3,4,5,6,7,8]}
        item_yaxis = {}
        for todays_data_row in todays_data_rows:
            # ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]

            item_xaxis.append(todays_data_row.get("get_data_time").strftime("%X"))
            # load1:10_load2:23_load3:34
            monitor_item_data = todays_data_row.get("data")
            monitor_item_data_list = monitor_item_data.split("_")  # ['load1:10', 'load2:23', 'load3:34']
            for per_item_data in monitor_item_data_list:
                per_item_data_list = per_item_data.split(":")
                item_name = per_item_data_list[0]  # load1
                data = per_item_data_list[1].strip("\n")
                if item_name not in item_yaxis:
                    item_yaxis[item_name] = [data]
                else:
                    item_yaxis[item_name].append(data)
        my_add_xaxis = '.add_xaxis(%s)' % item_xaxis
        my_add_yaxis = ''
        for item_y_key, item_y_value in item_yaxis.items():
            my_add_yaxis += '.add_yaxis("%s", %s)' % (item_y_key, item_y_value)
        #     这里是异步获取数据的类
        # 类名
        class_name = '%sView' % name
        # 类的父类
        class_bases = (View,)
        # 类体
        # 注意，这里还非要前面不能有空格
        class_body = """
def get(self, request, *args, **kwargs):
    c = (
        Line()
        %s
        %s
        .set_global_opts(title_opts=opts.TitleOpts(title="%s", subtitle="各项数据"),
                         datazoom_opts=opts.DataZoomOpts())
        .dump_options()
    )
    return MyJsonResponse(json.loads(c))
    """ % (my_add_xaxis, my_add_yaxis, name)
        class_dic = {}
        exec(class_body, globals(), class_dic)
        print("class_dic===", class_dic)
        # 步骤二：调用元类type（也可以自定义）来产生类Chinense
        # ViewClasss = type(class_name, class_bases, class_dic)  # 实例化type得到对象Foo，即我们用class定义的类Foo
        urlpatterns.append(re_path('%s/' % name, type(class_name, class_bases, class_dic).as_view()))
    # # ->常常出现在python函数定义的函数名后面，为函数添加元数据,描述函数的返回类型，从而方便开发人员使用。
    # def json_line_base() -> Line:
    # 这里不能使用->
    #     js = """
    #         $(function ()
    #             {get_bar_Data(chart_%s);
    #             setInterval(get_bar_Data, 2000);}
    #         );
    #         function get_bar_Data() {
    #             $.ajax({
    #                 type: 'GET',
    #                 url: 'http://10.0.0.61:8000/monitor/%s',
    #                 success: function (result)
    #                 {chart_%s.setOption(result.data);}});
    #             }
    #         """ % (name, name, name)
    #     js = "console.log('hello world')"
    #     由于有{}，所以就不用.format了,只能这样了
    #     不能用上面的方式，报错
    #     这里是动态添加到前端的js，动态定时获取显示的数据
        js = "$(function () {getData_%s(chart_%s);setInterval(getData_%s, %s);});" \
             "function getData_%s() {" \
             "$.ajax({" \
             "type: 'GET'," \
             "url: 'http://10.0.0.61:8000/monitor/%s'," \
             "success: function (result) " \
             "{chart_%s.setOption(result.data);}});}" % (name, name, name, time_interval, name, name, name)
        # 最初的函数，为前端添加js，初始数据

        func = """
def line_base():
    js = "{line_js}"
    c = (
        Line(init_opts=opts.InitOpts(chart_id='{name}',height="200px",width="100%"))
        {my_add_xaxis}
        {my_add_yaxis}
        .set_global_opts(title_opts=opts.TitleOpts(title="{name}"), datazoom_opts=opts.DataZoomOpts())
        .add_js_funcs(js)

    )
    return c
    """.format(name=name, my_add_xaxis=my_add_xaxis, my_add_yaxis=my_add_yaxis, line_js=js)

        foo_code = compile(func, "<string>", "exec")

        line_base = FunctionType(foo_code.co_consts[0], globals())

        page.add(line_base())
    return HttpResponse(page.render_embed())