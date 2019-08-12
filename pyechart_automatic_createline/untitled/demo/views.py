from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from random import randrange
from types import FunctionType
CurrentConfig.ONLINE_HOST = "http://10.0.0.61:8001/assets/"
# [root@m01 pyecharts-assets]# python3 -m http.server 8001&
# [1] 41184
# [root@m01 pyecharts-assets]# Serving HTTP on 0.0.0.0 port 8001 (http://0.0.0.0:8001/) ...
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates/monitor/templates/"))

from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Page,Grid,Scatter
# http://127.0.0.1:8000/demo/
def bar_base() -> Bar:
    js = """
    $(function () 
        {get_bar_Data(chart_bar_id);
        setInterval(get_bar_Data, 2000);}
    );
    function get_bar_Data() {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:8000/demo/bar',
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
# def line_base() -> Line:
#     js = "$(function () {getData(chart_qw);setInterval(getData, 2000);});function getData() {$.ajax({type: 'GET',url: 'http://127.0.0.1:8000/demo/line',success: function (result) {chart_qw.setOption(result.data);}});}"
#     c = (
#         Line(init_opts=opts.InitOpts(chart_id="qw",height="200px",width="100%"))
#         .add_xaxis(Faker.choose())
#         .add_yaxis("商家A", Faker.values())
#         .add_yaxis("商家B", Faker.values())
#         .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
#         .add_js_funcs(js)
#     )
#     return c

class LineView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(json_line_base()))
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


def json_bar_base() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts())
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"),
                         datazoom_opts=opts.DataZoomOpts())
        .dump_options()
    )
    return c
JsonResponse = json_response
JsonError = json_error
#
#
# class ChartView(View):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(json.loads(json_bar_base()))
#
# class IndexView(View):
#     def get(self, request, *args, **kwargs):
#         # return render(request,"index1.html")
#         return HttpResponse(content=open("./templates/index.html").read())
# ->常常出现在python函数定义的函数名后面，为函数添加元数据,描述函数的返回类型，从而方便开发人员使用。
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




cnt = 9


class ChartUpdateView(View):
    def get(self, request, *args, **kwargs):
        global cnt
        cnt = cnt + 1
        return JsonResponse({"name": "草莓", "value": randrange(0, 100)})

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/monitor/templates/index1.html").read())

def index(request):
    # # page.render()
    from demo.urls import urlpatterns
    from django import urls
    from django.urls import path, re_path
    class_name = 'BarView'
    # 类的父类
    class_bases = (View,)
    # 类体
    # 注意，这里还非要前面不能有空格
    class_body = """
def get(self, request, *args, **kwargs):
    return JsonResponse(json.loads(json_bar_base()))
    """
    class_dic = {}
    exec(class_body, globals(), class_dic)
    print("class_dic===", class_dic)
    # 步骤二：调用元类type（也可以自定义）来产生类Chinense
    BarViewClasss = type(class_name, class_bases, class_dic)  # 实例化type得到对象Foo，即我们用class定义的类Foo
    bar= "bar"
    urlpatterns.append(re_path('%s/'%bar, BarViewClasss.as_view()))
    urlpatterns.append(re_path('line/', LineView.as_view()))
    print("qwqwq", urlpatterns)
    # # ->常常出现在python函数定义的函数名后面，为函数添加元数据,描述函数的返回类型，从而方便开发人员使用。
    # def json_line_base() -> Line:
    # 这里不能使用->
    func = """
def line_base():
    js = "$(function () {getData(chart_qw);setInterval(getData, 2000);});function getData() {$.ajax({type: 'GET',url: 'http://127.0.0.1:8000/demo/line',success: function (result) {chart_qw.setOption(result.data);}});}"
    c = (
        Line(init_opts=opts.InitOpts(chart_id="qw",height="200px",width="100%"))
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
        .add_js_funcs(js)
        
    )
    return c
    """
    foo_code = compile(func, "<string>", "exec")
    print("--------------------------",foo_code.co_consts[0])
    line_base = FunctionType(foo_code.co_consts[0], globals())
    page = Page()
    page.add(line_base(),bar_base())

    return HttpResponse(page.render_embed())
