from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.http import JsonResponse


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
        # 获取前端传过来的用户名与密码
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # 到数据库中获取用户信息
        user_obj = User.objects.filter(username=user)
        res = {"user": None, "info": None}
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
    return render(request, "index.html")


@login_required
def logout(request):
    # 退出登录，删除session,cookie信息
    auth.logout(request)
    return redirect("/login/")