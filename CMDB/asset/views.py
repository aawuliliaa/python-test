from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from urllib.parse import unquote
from django.urls import reverse
from web.utils import *
from web.page import *
from asset.models import *
from asset.form import *


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
        # print("22222222222222222222222222222", request.COOKIES)
        if not request.COOKIES.get(request.path.replace("/", "")+"data_nums_per_page"):
            # 初次访问，还没有设置COOKIE，所以我们设置一个默认值
            request.COOKIES[request.path.replace("/", "")+"data_nums_per_page"] = 10
        # print("3333333333333333333",request.COOKIES.get(request.path.replace("/", "")+"data_nums_per_page"))

        if request.COOKIES.get(request.path.replace("/", "")+"search"):
            search_val = request.COOKIES.get(request.path.replace("/", "")+"search").strip()

            data_obj_set = data_obj_set.filter(Q(name__contains=unquote(search_val, "utf-8")) |
                                               Q(abs_name__contains=unquote(search_val, "utf-8")))
        data_page_info = my_page(data_obj_set, request.GET.get("page_num", 1),
                                 int(request.COOKIES.get(request.path.replace("/", "")+"data_nums_per_page")))
        return render(request, 'asset/env.html', locals())


class AddEnv(View):
    """
    添加环境信息
    """
    def get(self, request):
        left_label_dic = get_label(request)
        form = EnvironmentForm()
        return render(request, 'asset/add_edit_env.html', locals())

    def post(self, request):
        form = EnvironmentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse("asset:env"))


class DelEnv(View):
    """
    删除环境信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        Environment.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("asset:env"))


class EditEnv(View):

    edit_env=None

    def get(self, request, **kwargs):
        self.edit_env = Environment.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = EnvironmentForm(instance=self.edit_env)  # 接收实例对象
        return render(request, "asset/add_edit_env.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        form = EnvironmentForm(request.POST, instance=self.edit_env)  # 传递需要更新的对象
        if form.is_valid():
            form.save()  # edit_book.update(request.POST)
            # 去数据库中取出数据
        return redirect(reverse("asset:env"))