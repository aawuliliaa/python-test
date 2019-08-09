"""CMDB URL Configuration

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
from django.urls import path, re_path, include
from web import views
from django.views.static import serve
from CMDB import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    re_path(r'^api/', include('web.rest_urls')),
    path('privilege/', views.privilege, name="privilege"),
    path('role_export/', views.role_export, name="role_export"),
    # 监控配置与信息查看
    path('monitor/', include('monitor.urls', namespace="monitor")),
    # 定时任务
    path('crond/', include('crond.urls', namespace="crond")),
    # 资产信息
    path('asset/', include('asset.urls', namespace="asset")),
    # 任务信息
    path('task_manage/', include('task_manage.urls', namespace="task_manage")),
    # media配置:只有配置了这里，Index页面中才能显示出头像
    # 这里要注意，当url多了的时候，就会出现匹配的顺序问题，
    # 当不显示图片的时候，要查看下是否被上面的url给匹配了
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
