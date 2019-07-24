from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from web.utils import *
from web.page import *
from asset.models import *
from asset.form import *

# https://www.cnblogs.com/yuanchenqi/articles/8034442.html
# https://www.cnblogs.com/yuanchenqi/articles/7614921.html
# https://www.cnblogs.com/wupeiqi/articles/6144178.html


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
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
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
        left_label_dic = get_label(request)
        form = EnvironmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("asset:env"))
        return render(request, 'asset/add_edit_env.html', locals())


class DelEnv(View):
    """
    删除环境信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        Environment.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("asset:env"))


class EditEnv(View):
    """
    编辑功能就使用了modelform自带的逻辑，如果想自定义逻辑，可能还是使用form把
    """

    edit_env = None

    def get(self, request, **kwargs):
        self.edit_env = Environment.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = EnvironmentForm(instance=self.edit_env)  # 接收实例对象
        return render(request, "asset/add_edit_env.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        name = request.POST.get("name")
        abs_name = request.POST.get("abs_name")
        env_set = Environment.objects.filter(name=name, abs_name=abs_name)
        env_set.update(note=request.POST.get("note"))

        return redirect(reverse("asset:env"))


class SystemView(View):
    """
    系统信息
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

        data_obj_set = System.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("name", "abs_name", "operate_person__email"))
        return render(request, 'asset/system.html', locals())


class AddSystem(View):
    """
    添加系统信息
    """

    def get(self, request):
        left_label_dic = get_label(request)
        form = SystemForm()
        return render(request, 'asset/add_edit_system.html', locals())

    def post(self, request):
        # 添加的时候不需要手动插入数据到关联表中，form会帮我们自动处理
        left_label_dic = get_label(request)
        form = SystemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("asset:system"))
        return render(request, 'asset/add_edit_system.html', locals())


class EditSystem(View):

    edit_system = None

    def get(self, request, **kwargs):
        self.edit_system = System.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = SystemForm(instance=self.edit_system)  # 接收实例对象
        return render(request, "asset/add_edit_system.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        name = request.POST.get("name")
        abs_name = request.POST.get("abs_name")
        sys_set = System.objects.filter(name=name, abs_name=abs_name)
        sys_obj = sys_set.first()
        sys_set.update(note=request.POST.get("note"), operate_person_id=request.POST.get("operate_person"))
        # 设置环境信息
        environment_list = request.POST.getlist("environment")
        # print("====================================", environment_list)  # ['1', '2', '3']
        sys_obj.environment.set(environment_list)
        return redirect(reverse("asset:system"))


class DelSystem(View):
    """
    删除系统信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        System.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("asset:system"))


class ApplicationView(View):
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

        data_obj_set = Application.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("name", "middleware"))
        return render(request, 'asset/application.html', locals())


class AddApplication(View):
    """
    添加系统信息
    """

    def get(self, request):
        left_label_dic = get_label(request)
        form = ApplicationForm()
        return render(request, 'asset/add_edit_application.html', locals())

    def post(self, request):
        # 添加的时候不需要手动插入数据到关联表中，form会帮我们自动处理
        left_label_dic = get_label(request)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("asset:application"))
        return render(request, 'asset/add_edit_application.html', locals())


class EditApplication(View):

    edit_application = None

    def get(self, request, **kwargs):
        self.edit_application = Application.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = ApplicationForm(instance=self.edit_application)  # 接收实例对象
        return render(request, "asset/add_edit_application.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        middleware = request.POST.get("middleware")
        name = request.POST.get("name")
        app_set = Application.objects.filter(name=name, middleware=middleware)
        app_set.update(note=request.POST.get("note"))
        return redirect(reverse("asset:application"))


class DelApplication(View):
    """
    删除应用信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        Application.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("asset:application"))