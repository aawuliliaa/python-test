from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
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
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()

        data_obj_set = Environment.objects.all()

        data_page_info = return_show_data(request, data_obj_set, *("name", "abs_name"))
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

    edit_env = None

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