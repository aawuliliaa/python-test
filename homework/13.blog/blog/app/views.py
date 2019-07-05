from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import F
from django.db import transaction
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
    if request.method == "POST":
        # print(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': [],'username': ['eee'],
        # 'password': ['1234567'], 're_password': ['1234567'], 'email': ['eee@qq.com']}>
        form = UserForm(request.POST)
        response = {"user": None, "msg": None}
        if form.is_valid():
            username = form.cleaned_data.get("username")
            response["user"] = username
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            # print("--------------",type(avatar_obj)) <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
            # models.FileField接收文件对象，把文件下载到相应的位置，保存文件名为字段值
            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
            UserInfo.objects.create_user(username=username, password=password, email=email, **extra)
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
    form_obj = UserForm()
    return render(request, "register.html", locals())


def home_site(request, username, **kwargs):
    """
    个人站点页面
    :param request:
    :param username:
    :return:
    """
    article_obj_list = Article.objects.filter(user__username=username)

    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "category":
            article_obj_list = article_obj_list.filter(category__title=param)
        elif condition == "tag":
            article_obj_list = article_obj_list.filter(tags__title=param)
        elif condition == "archive":

            year, month = param.split("-")
            article_obj_list = article_obj_list.filter(create_time__year=year, create_time__month=month)

    return render(request, "home-site.html", {"username": username, "article_obj_list": article_obj_list})


def article_detail(request, username, article_id):
    """
    文章详情页
    :param request:
    :param article_id:
    :param username:
    :return:
    """
    article_obj = Article.objects.get(pk=article_id)
    return render(request, "article_detail.html", locals())


def get_comment_tree(request):
    """
    展示评论树
    :param request:
    :return:
    """
    article_id = request.GET.get("article_id")
    # 把queryset
    comment_list = list(Comment.objects.filter(article_id=article_id).
                        values("pk", "content", "parent_comment_id", "user__username"))
    # 非字典传送时，需要设置safe为false
    return JsonResponse(comment_list, safe=False)


def commit_comment(request):
    """
    提交评论
    :param request:
    :return:
    """
    result = {"success": None}
    article_id = int(request.POST.get("article_id"))
    parent_comment_id = request.POST.get("parent_comment_id")
    if parent_comment_id:
        reply_user = request.POST.get("reply_user")
        comment_content = request.POST.get("comment_content").split(reply_user)[1].strip()
    else:
        comment_content = request.POST.get("comment_content")
    #     事务操作
    with transaction.atomic():
        comment_obj = Comment.objects.create(article_id=article_id,
                                             content=comment_content,
                                             parent_comment_id=parent_comment_id, user_id=request.user.pk)
        Article.objects.filter(id=article_id).update(comment_count=F("comment_count") + 1)
    result["success"] = True
    result["pk"] = comment_obj.pk
    result["content"] = comment_content
    result["parent_comment_id"] = parent_comment_id
    result["user__username"] = comment_obj.user.username
    return JsonResponse(result)


def up_down(request):
    """
    点赞与反对按钮事件
    :param request:
    :return:
    """
    result = {"success": None}
    article_id = int(request.POST.get("article_id"))
    up_down = request.POST.get("up_down")
    user_id = request.user.pk
    up_down_obj = ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id)
    # 某个人对某文章没有评论过，就进行下面的操作
    if not up_down_obj:

        article_obj = Article.objects.filter(id=article_id)
        if up_down == "down":
            article_obj.update(up_count=F("down_count") + 1)
            is_up = False
        else:
            article_obj.update(up_count=F("up_count") + 1)
            is_up = True
        ArticleUpDown.objects.create(is_up=is_up, article_id=article_id, user_id=user_id)
        result["success"] = True
    return JsonResponse(result)


def back_manage(request):
    return render(request, "back_manage/index.html")