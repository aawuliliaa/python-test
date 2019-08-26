"""PHM URL Configuration

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
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from stark.service.StarkSite import site

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^rbac/', include('rbac.urls', namespace='rbac')),
    re_path(r'^sign/', include('sign.urls', namespace='sign')),
    re_path(r'^problem/', include('problem.urls', namespace='problem')),
    re_path(r'^stark/', site.urls),
    # media配置:只有配置了这里，Index页面中才能显示出头像
    # 这里要注意，当url多了的时候，就会出现匹配的顺序问题，
    # 当不显示图片的时候，要查看下是否被上面的url给匹配了
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
# print("----------------------",site.urls)
#  ([<URLResolver <URLPattern list> (None:None) '^problem/problem'>], 'stark', 'stark')