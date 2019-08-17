
from django.contrib import admin
from django.urls import path, re_path
from stark.service.v1 import site
# 方式三：
#     urlpatterns = [
#         url(r'^web/', ([
#             url(r'^index/', views.index),
#             url(r'^home/', views.home),
#         ], app_name, namespace)), # 第一个参数是urls文件对象，通过此对象可以获取urls.patterns获取分发的路由。
#     ]

# site.urls------------ ([<URLPattern 'app01/depart/list/$'>,
# <URLPattern 'app01/depart/add/$'>,
# <URLPattern 'app01/depart/change/(\d+)/$'>,
# <URLPattern 'app01/depart/del/(\d+)/$'>,
# <URLPattern 'app01/userinfo/list/$'>,
# <URLPattern 'app01/userinfo/add/$'>,
# <URLPattern 'app01/userinfo/change/(\d+)/$'>,
# <URLPattern 'app01/userinfo/del/(\d+)/$'>,
# <URLPattern 'app02/host/list/$'>,
# <URLPattern 'app02/host/add/$'>,
# <URLPattern 'app02/host/change/(\d+)/$'>,
# <URLPattern 'app02/host/del/(\d+)/$'>,
# <URLPattern 'app02/role/list/$'>,
# <URLPattern 'app02/role/add/$'>,
# <URLPattern 'app02/role/change/(\d+)/$'>,
# <URLPattern 'app02/role/del/(\d+)/$'>], 'stark', 'stark')
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^stark/', site.urls),
]
