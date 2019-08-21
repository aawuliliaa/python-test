from django.db import models
# from django.contrib.auth.models import AbstractUser


class Menu(models.Model):
    """
    一级菜单表
    """
    title = models.CharField(verbose_name="菜单名称", help_text="一级菜单名称", max_length=32, default="")
    icon = models.CharField(verbose_name="图标", help_text="菜单的图标样式", max_length=32, default="")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "一级菜单表"
        verbose_name_plural = '一级菜单表'

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表，包含二级菜单和二级菜单中的增删改查按钮
    """
    title = models.CharField(verbose_name="标题", max_length=32, default="")
    url = models.CharField(verbose_name="含有正则表达式的URL，urls.py中配置的", max_length=255, default="")
    name = models.CharField(verbose_name="URL别名", max_length=32, unique=True, default="")
    menu = models.ForeignKey(verbose_name="所属菜单",
                             to=Menu,
                             help_text="该项不为空，则是二级菜单，为空时，pid不为空，是二级菜单中的按钮",
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)
    pid = models.ForeignKey("self",
                            verbose_name="所属的二级菜单",
                            help_text="自关联字段，二级菜单中的按钮，要设置pid，设置所属的二级菜单",
                            null=True, blank=True, related_name="parent_menu", on_delete=models.CASCADE)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "权限表"
        verbose_name_plural = '权限表'

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(verbose_name="角色名称", max_length=32, default="")
    permissions = models.ManyToManyField(verbose_name="角色拥有的权限",
                                         blank=True,
                                         to=Permission)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "角色表"
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title


# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    email = models.CharField(verbose_name="邮箱", max_length=32)
    roles = models.ManyToManyField(verbose_name="该用户拥有的角色", to=Role, blank=True)

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
