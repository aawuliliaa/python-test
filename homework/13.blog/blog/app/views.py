from django.shortcuts import render, HttpResponse, redirect
import json
from django.contrib import auth
from geetest import GeetestLib
from app.models import *
from app.my_form import UserForm
# Create your views here.
# 这里是滑动验证处使用的
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

def pcgetcaptcha(request):
    """
    滑动验证
    :param request:
    :return:
    """
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def pcajax_validate(request):
    """
    滑动验证
    :param request:
    :return:
    """
    if request.method == "POST":
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        result = {"status": "success", "user": None} if result else {"status": "fail", "user": None}
        # 验证用户名和密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            result["user"] = username
        return HttpResponse(json.dumps(result))
    return HttpResponse("error")


def login(request):
    """
    登录
    :param request:
    :return:
    """
    # if request.method == "POST":
    #     result = {"user": None}
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user = auth.authenticate(username=username, password=password)
    #     if user:
    #         auth.login(request, user)
    #         result["user"] = username
    #     return HttpResponse(json.dumps(result))
    return render(request, "login.html")


def logout(request):
    """
    退出
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect("/index/")


def index(request):
    """
    展示全部文章的内容，首页。不管是否登录，都能查看到这个页面
    :param request:
    :return:
    """
    article_obj_list = Article.objects.all()
    return render(request, "index.html", locals())


def register(request):
    """
    注册
    :param request:
    :return:
    """
    form_obj = UserForm()
    return render(request, "register.html", locals())


