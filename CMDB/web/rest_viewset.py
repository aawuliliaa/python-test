from rest_framework import viewsets
from web import models

from web import rest_searializer


# ViewSets define the view behavior.
class MyUserViewSet(viewsets.ModelViewSet):
    queryset = models.MyUser.objects.all()
    serializer_class = rest_searializer.MyUserSerializer


class PrivilegeViewSet(viewsets.ModelViewSet):
    queryset = models.Privilege.objects.all()
    serializer_class = rest_searializer.PrivilegeSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = rest_searializer.RoleSerializer

