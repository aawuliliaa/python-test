from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "login.html")
def index(request):
    """
    展示全部文章的内容，首页。不管是否登录，都能查看到这个页面
    :param request:
    :return:
    """
    return render(request, "index.html")