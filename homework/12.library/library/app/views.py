from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User


def login(request):
    # 登录函数
    return render(request, "login.html")


def register(request):
    # 注册函数
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    User.objects.get(username=user)
    return ""