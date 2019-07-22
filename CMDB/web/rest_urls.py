from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path,re_path
from web import rest_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'MyUsers', rest_view.MyUserViewSet)
router.register(r'Privileges', rest_view.PrivilegeViewSet)
# router.register(r'Role', rest_viewset.RolekView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'Role', rest_view.RoleView.as_view()),
    # rest提交数据测试
    path('rest_post_test/', rest_view.TestAuthView.as_view(), name="rest_post_test"),
    # 会有登录的功能，可以创建数据
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]