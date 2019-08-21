from django.db import models
# from django.contrib.auth.models import AbstractUser
class Role(models.Model):
    pass
# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    email = models.CharField(verbose_name="邮箱", max_length=32)
    # roles = models.ManyToManyField(verbose_name="该用户拥有的角色", to=Role, blank=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "用户表"
        verbose_name_plural = '用户表'
        abstract = True
    #     class Meta:
    #         # django以后再做数据库迁移时，不再为UserInfo类创建相关的表以及表结构了。
    #         # 此类可以当做"父类"，被其他Model类继承。
    #         abstract = True

    def __str__(self):
        return self.name