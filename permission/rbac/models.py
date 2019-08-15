from django.db import models

# Create your models here.
class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='一级菜单名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32, null=True, blank=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "菜单表"
        verbose_name_plural = '菜单表'

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name="标题", max_length=32)
    url = models.CharField(verbose_name="含有正则的URL", max_length=255)
    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True, default="")
    menu = models.ForeignKey(verbose_name='所属菜单',
                             to='Menu',
                             null=True,
                             blank=True,
                             help_text='null表示不是菜单;非null表示是二级菜单',
                             on_delete=models.CASCADE)
    pid = models.ForeignKey("self", verbose_name="关联的权限", null=True, blank=True, related_name='parents',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单',
                            on_delete=models.CASCADE)

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
    title = models.CharField(verbose_name="角色名称", max_length=32)
    permissions = models.ManyToManyField(verbose_name="该角色拥有的权限", to=Permission, blank=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "角色表"
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.name