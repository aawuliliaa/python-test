from rest_framework import routers
from django.conf.urls import url, include
from web import rest_viewset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'MyUsers', rest_viewset.MyUserViewSet)
router.register(r'Privileges', rest_viewset.PrivilegeViewSet)
router.register(r'Role', rest_viewset.RoleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # 会有登录的功能，可以创建数据
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]