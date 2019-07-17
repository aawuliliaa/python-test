
from web import models
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.


# 定义了一个表现形式
# 被关联的表也要定义，这样role表才能取到关联表中的数据

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        # 关联的表
        model = models.MyUser
        # 要展示哪些字段给前端
        fields = ('name', 'email', 'is_admin', 'create_time', 'update_time')


class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Privilege
        fields = ('id', 'name', 'note', 'create_time', 'update_time')


# HyperlinkedModelSerializer关联表以url形式显示
# ModelSerializer显示关联表的ID值
class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Role
        fields = ('id', 'name', 'code', 'parent_menu_name', 'child_menu_name', 'url',
                  'note', 'users', 'privileges', 'create_time', 'update_time')
        # 列出关联表中的详细数据
        # depth = 2
