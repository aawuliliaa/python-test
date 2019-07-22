
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
        # fields = ('name', 'email', 'is_admin', 'create_time', 'update_time')
        fields = "__all__"


class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Privilege
        # fields = ('id', 'name', 'note', 'create_time', 'update_time')
        fields = "__all__"


# HyperlinkedModelSerializer关联表以url形式显示
# ModelSerializer显示关联表的ID值
# 它简单的默认实现了.update()以及.create()方法,提交请求时，会自动创建数据和更新数据
class RoleSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        # obj是当前序列化的book对象
        users_query_set = obj.users.all()
        # 外键关联的对象有很多字段我们是用不到的~都传给前端会有数据冗余~就需要我们自己去定制序列化外键对象的哪些字段~~
        return [{"id": user_obj.pk, "name": user_obj.name} for user_obj in users_query_set]

    class Meta:
        model = models.Role
        #  # 字段是有序的
        # fields = ('id', 'name', 'code', 'parent_menu_name', 'child_menu_name', 'url',
        #           'note', 'users', 'privileges', 'create_time', 'update_time')
        fields = "__all__"

        # 列出关联表中的详细数据
        # 由于设置了depth,那么关联字段会变为只读状态，
        # 但是由于我们发送post请求提交数据，patch请求局部更新数据时，都需要修改，所以不能加此参数
        # depth = 2
