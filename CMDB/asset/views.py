from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
import os
from web.password_crypt import encrypt_p, decrypt_p
from web.utils import *
from web.page import *
from asset.models import *
from asset.form import *
from CMDB import settings

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
        left_label_dic = get_label(request)
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
        left_label_dic = get_label(request)
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
        left_label_dic = get_label(request)
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


class HostLoginUserView(View):
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

        data_obj_set = HostLoginUser.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("name", "name_info"))
        return render(request, 'asset/host_login_user.html', locals())


class AddHostLoginUser(View):
    """
    添加系统信息
    """

    def get(self, request):
        left_label_dic = get_label(request)
        form = HostLoginUserForm()
        return render(request, 'asset/add_edit_host_login_user.html', locals())

    def post(self, request):
        # 添加的时候不需要手动插入数据到关联表中，form会帮我们自动处理
        left_label_dic = get_label(request)
        # modelform上传文件
        form = HostLoginUserForm(request.POST, request.FILES)
        name = request.POST.get("name")
        name_info = request.POST.get("name_info")
        password = request.POST.get("password")
        if form.is_valid():
            form.save()
            HostLoginUser.objects.filter(name=name, name_info=name_info).update(password=encrypt_p(password))
            return redirect(reverse("asset:host_login_user"))
        return render(request, 'asset/add_edit_host_login_user.html', locals())


class EditHostLoginUser(View):

    edit_host_login_user = None

    def get(self, request, **kwargs):
        left_label_dic = get_label(request)
        self.edit_host_login_user = HostLoginUser.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = HostLoginUserForm(instance=self.edit_host_login_user)  # 接收实例对象
        return render(request, "asset/add_edit_host_login_user.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        name_info = request.POST.get("name_info")
        name = request.POST.get("name")
        user_set = HostLoginUser.objects.filter(name=name, name_info=name_info)

        file_obj = request.FILES.get("key_file")
        # 如果没有上传文件,就更新数据
        if not file_obj:
            user_set.update(password=request.POST.get("password"), expire_date=request.POST.get("expire_date"),)
        else:
            # 如果上传了文件，就把旧数据删除，创建新数据，create_time保留
            create_time = user_set.first().create_time
            file_path = user_set.first().key_file  # 这是一个FileField类
            file_abs_path = os.path.join(settings.MEDIA_ROOT, file_path.name)
            os.remove(file_abs_path)
            user_set.delete()

            # 由于update方法不能创建文件，但是create可以在upload路径下创建文件，
            # 为了不处理麻烦的路径问题，把原数据删除，创建新的数据
            HostLoginUser.objects.create(name_info=name_info, name=name, create_time=create_time,
                                         password=request.POST.get("password"),
                                         key_file=file_obj,
                                         expire_date=request.POST.get("expire_date"))
        return redirect(reverse("asset:host_login_user"))


class DelHostLoginUser(View):
    """
    删除登录用户信息，同时把上传的文件也删除
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        user_set = HostLoginUser.objects.filter(id=kwargs.get("pk"))

        file_path = user_set.first().key_file  # 这是一个FileField类
        if file_path:
            file_abs_path = os.path.join(settings.MEDIA_ROOT, file_path.name)
            # 删除文件
            os.remove(file_abs_path)
            # 删除数据
        user_set.delete()
        return redirect(reverse("asset:host_login_user"))


class HostView(View):
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

        data_obj_set = Host.objects.all()
        # 这里和面的*("name", "abs_name")是前端的搜索功能，这里是搜索的字段
        data_page_info = return_show_data(request, data_obj_set, *("ip", "hostname"))
        return render(request, 'asset/host.html', locals())


class AddHost(View):
    """
    添加系统信息
    """

    def get(self, request):
        left_label_dic = get_label(request)
        form = HostForm()
        return render(request, 'asset/add_edit_host.html', locals())

    def post(self, request):
        # 添加的时候不需要手动插入数据到关联表中，form会帮我们自动处理
        left_label_dic = get_label(request)
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("asset:host"))
        return render(request, 'asset/add_edit_host.html', locals())


class EditHost(View):
    """
    编辑主机信息
    """

    edit_host = None

    def get(self, request, **kwargs):
        left_label_dic = get_label(request)
        self.edit_host = Host.objects.filter(pk=kwargs.get("pk")).first()
        # 创建form对象，传入参数就可以显示之前客户写入的值,ModelForm具备instance参数
        form = HostForm(instance=self.edit_host)  # 接收实例对象
        return render(request, "asset/add_edit_host.html", locals())

    def post(self, request, **kwargs):
        # 这里需要注意，由于设置了联合主键，如果修改的时候修改成与现有的内容重复了，会放弃修改，
        # 现象是提交的时候不会报错，只是你会发现没有修改成功
        # 我这里设置了联合主键name和abs_name,发现如果这两个值不修改，修改其他内容是修改不成功的
        # 因为会先去数据库中查询，如果存在，就报已经存在
        # 但是我不希望这样，所以就自己在前端设置name和abs_name不可编辑，其他内容手动插入，就没有使用form了
        # 这样既能利用modelform的优势，也能灵活操作。
        # 由于不可为空和长度限制已经在前端限制好了，后端就不需要做检查了
        left_label_dic = get_label(request)

        ip = request.POST.get("ip")
        host_set = Host.objects.filter(ip=ip)
        host_obj = host_set.first()
        host_set.update(note=request.POST.get("note"),
                        MAC=request.POST.get("MAC"),
                        hostname=request.POST.get("hostname"),
                        cpu=request.POST.get("cpu"),
                        mem=request.POST.get("mem"),
                        disk=request.POST.get("disk"),
                        expire_date=request.POST.get("expire_date"),
                        system_id=request.POST.get("system"),
                        environment_id=request.POST.get("environment")
                        )
        application_list = request.POST.getlist("application")
        login_user_list = request.POST.getlist("login_user")
        host_obj.application.set(application_list)
        host_obj.login_user.set(login_user_list)
        return redirect(reverse("asset:host"))


class DelHost(View):
    """
    删除应用信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        Host.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("asset:host"))
