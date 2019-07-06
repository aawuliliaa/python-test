"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views
from django.views.static import serve
from blog import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    # 这里是滑动验证码处使用的ajax
    re_path(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
    re_path(r'^pc-geetest/ajax_validate', views.pcajax_validate, name='pcajax_validate'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    # 获取评论树
    path('get_comment_tree/', views.get_comment_tree),
    # 提交评论
    path('commit_comment/', views.commit_comment),
    # 点赞按钮
    path('up_down/', views.up_down),
    re_path('^$', views.index),
    path('back_manage/', views.back_manage, name="back_manage"),
    path('add_article/', views.add_article),
    # kindeditor编辑器中的图片上传
    path('upload/', views.upload),
    # 删除文章分类或标签
    path('del_classes/', views.del_classes),
    path('add_classes/', views.add_classes),


    # 这里如果不在index/后加个$结尾，访问index/的时候，，页面的中图片就不显示
    re_path('index/$', views.index, name="index"),
    re_path('^(?P<username>[a-zA-Z]+)/articles/(?P<article_id>[0-9]+)$', views.article_detail),
    # media配置:只有配置了这里，Index页面中才能显示出头像
    # 这里要注意，当url多了的时候，就会出现匹配的顺序问题，
    # 当不显示图片的时候，要查看下是否被上面的url给匹配了
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^(?P<username>[a-zA-Z]+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$", views.home_site),
    re_path('^(?P<username>[a-zA-Z]+)/$', views.home_site),

]
