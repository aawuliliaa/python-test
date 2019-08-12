from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.urls import reverse
import time, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from urllib.parse import unquote
from web.reg_form import UserForm
from web.models import *
from web.utils import *
from web.page import *
from crond.tasks import reset_host_login_user_password
from monitor.models import WarnTable
from asset.models import Host

@login_required
def index(request):
    """
    index首页
    :param request:
    :return:
    """
    # 左侧菜单栏

    # reset_host_login_user_password()
    left_label_dic = get_label(request)
    now = time.localtime()
    # 显示当天的告警信息
    # 测试的时候使用的
    # 显示当日的告警信息
    # datetime字段，查询当日数据
    warn_table_set = WarnTable.objects.filter(get_data_time__gte=datetime.datetime.now().date()).order_by("-get_data_time")
    print("========================", warn_table_set)

    # 显示近一周的数据
    host_update_set = Host.objects.filter(update_time__gt=datetime.datetime.now() - datetime.timedelta(7))\
        .order_by("-update_time")
    return render(request, "index.html", locals())


def login(request):
    """
    注册功能
    :param request:
    :return:
    """
    if request.method == 'POST':
        res = {"user": None, "info": None}
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            res["user"] = email
        else:
            res["info"] = "用户名或密码不正确"
        return JsonResponse(res)

    return render(request, "login.html")


@login_required
def logout(request):
    """
    退出
    :param request:
    :return:
    """
    auth.logout(request)
    response = redirect(reverse("login"))
    # response.delete_cookie("data_nums_per_page")
    # response.delete_cookie("role_search")
    # response.delete_cookie("env_data_nums_per_page")
    # response.delete_cookie("env_role_search")
    # response.cookies.clear()

    return response


def register(request):
    """
    注册
    :param request:
    :return:
    """
    print(request.get_full_path())
    if request.method == "POST":
        # print(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': [],'username': ['eee'],
        # 'password': ['1234567'], 're_password': ['1234567'], 'email': ['eee@qq.com']}>
        form = UserForm(request.POST)
        print(request.POST)
        response = {"user": None, "msg": None}
        # 所有的form字段验证通过
        if form.is_valid():

            username = form.cleaned_data.get("username")
            response["user"] = username
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            # 获取文件对象，由于models中使用的是FileField，所以就不需要自己手动操作图片内容了
            avatar_obj = request.FILES.get("avatar")
            # print("--------------",type(avatar_obj)) <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
            # models.FileField接收文件对象，把文件下载到相应的位置，保存文件名为字段值
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
            else:
                extra["avatar"] = "avatar/default.png"
            #     新加用户
            MyUser.objects.create_user(name=username, password=password, email=email, **extra)
        else:
            # 要清楚form.errors数据类型，这样在前端才能用合适的方式循环使用数据
            # print("form.errors----", form.errors)
            # print("type(form.errors)----", type(form.errors))  # <class 'django.forms.utils.ErrorDict'>
            # print("form.errors.get('name')----", form.errors.get("name"))
            # <ul class="errorlist"><li>该字段不能为空</li></ul>
            # print("type(form.errors.get('name'))----",
            #       type(form.errors.get("name")))  # <class 'django.forms.utils.ErrorList'>
            # print("form.errors.get('name')[0]----", form.errors.get("name")[0])
            # print("form.cleaned_data---------", form.cleaned_data)
            #     {'pwd': '1234', 'email': '123@qq.com', 'tel': '123'}

            response["msg"] = form.errors
        return JsonResponse(response)
    elif request.method == "GET":
        form_obj = UserForm()
        return render(request, "register.html", locals())


@login_required
def privilege(request):
    """
    展示当前用户的角色权限信息
    :param request:
    :return:
    """
    # 左侧菜单栏
    # 批量创建测试数据
    # list = []
    # for i in range(0,101):
    #     item = Role(name="role_%s" % i, parent_menu_name="role_%s" % i,
    #     child_menu_name="role_%s" % i,url="role_%s" % i)
    #     list.append(item)
    #
    # Role.objects.bulk_create(list)

    left_label_dic = get_label(request)
    # print("mmmmmmmmmmmmmmmmmmmmmmm",request.path)# /privilege/
    role_obj = Role.objects.filter(url=request.path).first()
    if request.user.is_admin:
        data_obj_set = Role.objects.all().order_by('id')
    else:
        data_obj_set = Role.objects.filter(users__email=request.user.email).all().order_by('id')
        # 展示一些分页数据，供前端渲染使用
    #
    # if request.COOKIES.get(request.path.replace("/", "") + "search"):
    #     search_val = request.COOKIES.get(request.path.replace("/", "") + "search").strip()
    #
    #     data_obj_set = data_obj_set.filter(Q(users__email__contains=search_val) |
    #                                        Q(name__contains=unquote(search_val, "utf-8")) |
    #                                        Q(code__contains=unquote(search_val, "utf-8")))
    # data_page_info = my_page(data_obj_set, request.GET.get("page_num", 1),
    #                          int(request.COOKIES.get(request.path.replace("/", "") + "data_nums_per_page")))
    data_page_info = return_show_data(request, data_obj_set, *("users__email", "name", "code"))
    return render(request, 'privilege/privilege.html', locals())


def role_export(request):
    """
    角色权限数据导出
    :param request:
    :return:
    """
    if request.user.is_admin:
        role_obj_set = Role.objects.all().order_by('id')
    else:
        role_obj_set = Role.objects.filter(users__email=request.user.email).all().order_by('id')

    export_datas = list(role_obj_set.values_list("users__email", "name", "parent_menu_name",
                                                 "child_menu_name", "url", "privileges__name"))

    filename = 'roles.csv'
    header = ['用户名', '角色名称', '父级菜单名', '子级菜单名', 'url路径', '权限']
    response = export(filename, export_datas, header)
    return response


