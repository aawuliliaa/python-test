#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from sign.forms.reg_form import UserForm
from sign.models import UserInfo
from rbac.service.init_permission import init_permission

def index(request):
    return render(request, "sign/base.html")


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
        user = UserInfo.objects.filter(email=email, password=password).first()
        if user:
            # auth.login(request, user)
            request.session["current_user"] = {"email": email, "avatar": user.avatar.name}
            res["user"] = email
            # 初始化权限信息，把可访问的菜单信息存到session中
            init_permission(request, user)
        else:
            res["info"] = "用户名或密码不正确"
        return JsonResponse(res)

    return render(request, "sign/login.html")


def logout(request):
    """
    退出
    :param request:
    :return:
    """
    del request.session["current_user"]
    # response.delete_cookie("data_nums_per_page")
    # response.delete_cookie("role_search")
    # response.delete_cookie("env_data_nums_per_page")
    # response.delete_cookie("env_role_search")
    # response.cookies.clear()

    return redirect(reverse("sign:login"))


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
            UserInfo.objects.create(name=username, password=password, email=email, **extra)
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
        return render(request, "sign/register.html", locals())