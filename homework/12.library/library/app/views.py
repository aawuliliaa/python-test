from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import auth
import json
from app.models import *


def login(request):
    # 登录函数
    if request.method == "POST":
        res = {"user": None, "info": None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user_obj = User.objects.filter(username=user)
        # 用户存在
        if user_obj:
            # 验证用户名和密码是否正确
            auth_user_obj = auth.authenticate(username=user, password=pwd)
            if auth_user_obj:
                # 验证通过
                auth.login(request, auth_user_obj)

                res["user"] = user
                # 登录成功后，设置返回首页的url,由于多处使用，所以防在了session中
                request.session["back_url"] = "/index/"

            else:
                    res["user"] = user
                    res["info"] = "密码错误！"

        else:
            # 用户不存在时
            res["info"] = "用户不存在！"
        #     这种方式可以传中文到前端
        return JsonResponse(res)

    return render(request, "login.html")


def register(request):
    # 注册函数
    if request.method == "POST":
        res = {"user": None, "info": None}
        # 获取前端传过来的用户名与密码
        user = request.POST.get("user").strip()
        pwd = request.POST.get("pwd").strip()
        if user == "" or pwd == "":
            res["info"] = "user or password can not be null!"
            return HttpResponse(json.dumps(res))
        # 到数据库中获取用户信息
        user_obj = User.objects.filter(username=user)

        # 如果该用户已经存在，返回信息，不存在，插入该用户信息到数据库
        if user_obj:
            res["info"] = "user already exist!"

            return HttpResponse(json.dumps(res))
        # 用户不存在，就创建该用户
        User.objects.create_user(username=user, password=pwd)
        # 创建成功
        res["user"] = user
        # 这种方式不能传中文，前端会解析报错
        return HttpResponse(json.dumps(res))

# 需要auth.login()之后，才允许登录。auth.login会设置相关信息到session中
@login_required
def index(request):
    # 展示信息页面
    logout_url = "/logout/"
    author_list = Author.objects.all()

    return render(request, "index.html", locals())


@login_required
def logout(request):
    # 退出登录，删除session,cookie信息
    auth.logout(request)
    return redirect("/login/")


def add_author(request):
    # 添加作者信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        author_name = request.POST.get("author_name").strip()
        author_age = request.POST.get("author_age").strip()
        if author_name == "" or author_age == "":
            res["info"] = "作者名或年龄不能为空"
        elif not author_age.isnumeric():
            res["info"] = "年龄必须是数字"
        else:
            Author.objects.create(name=author_name, age=author_age)
            res["success"] = True
            res["info"] = "%s 作者添加成功" % author_name
        return JsonResponse(res)


def edit_author(request, author_id):
    return HttpResponse("")


def show_author(request, author_id):
    author_id = int(author_id)
    author_obj = Author.objects.get(id=author_id)
    author_book_list = Book.objects.filter(authors__id=author_id)

    return render(request, "author_book.html", locals())


def del_author(request, author_id):
    return HttpResponse("")