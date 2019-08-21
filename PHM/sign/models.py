from django.db import models
from rbac.models import UserInfo  as RbacUserInfo
# Create your models here.

class UserInfo(RbacUserInfo):
    """
    员工表
    """
    # 该字段存放的是用户头像的路径
    avatar = models.FileField(upload_to="avatar/", default="avatar/default.png", verbose_name="头像")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)


    def __str__(self):
        return self.name