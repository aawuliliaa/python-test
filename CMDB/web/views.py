from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from web.reg_form import UserForm
from web.models import *
from web.utils import *
from web.page import *
# Create your views here.


@login_required
def index(request):
    """
    index首页
    :param request:
    :return:
    """
    # 左侧菜单栏
    left_label_dic = get_label(request)
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
    auth.logout(request)
    return redirect(reverse("login"))


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
    if request.user.is_admin:
        role_obj_set = Role.objects.all().order_by('id')
    else:
        role_obj_set = Role.objects.filter(users__email=request.user.email).all().order_by('id')
        # 展示一些分页数据，供前端渲染使用
    if not request.COOKIES.get("data_nums_per_page"):
        request.COOKIES["data_nums_per_page"] = 10
    data_page_info = my_page(role_obj_set, request.GET.get("page_num", 1), int(request.COOKIES.get("data_nums_per_page")))

    return render(request, 'privilege/privilege.html', locals())