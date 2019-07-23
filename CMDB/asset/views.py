from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from urllib.parse import unquote
from web.utils import *
from web.page import *
from asset.models import *


class Env(View):
    """
    环境信息
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
        # print("mmmmmmmmmmmmmmmmmmmmmmm",request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()

        data_obj_set = Environment.objects.all()
        # 展示一些分页数据，供前端渲染使用
        if not request.COOKIES.get("env_data_nums_per_page"):
            # 初次访问，还没有设置COOKIE，所以我们设置一个默认值
            request.COOKIES["env_data_nums_per_page"] = 10
        if request.COOKIES.get("env_search"):
            search_val = request.COOKIES.get("env_search").strip()

            data_obj_set = data_obj_set.filter(Q(name__contains=unquote(search_val, "utf-8")) |
                                               Q(abs_name__contains=unquote(search_val, "utf-8")))
        data_page_info = my_page(data_obj_set, request.GET.get("page_num", 1),
                                 int(request.COOKIES.get("env_data_nums_per_page")))
        return render(request, 'asset/env.html', locals())

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')