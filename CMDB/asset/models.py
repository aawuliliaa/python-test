# from django.db import models
import random
from web.models import *
import time


class Environment(models.Model):
    """
    环境信息
    测试环境，预部署环境，生产环境。。
    """
    name = models.CharField(verbose_name="环境名", max_length=32)
    abs_name = models.CharField(verbose_name="环境名简称", max_length=32)
    note = models.CharField(verbose_name="环境名备注信息", max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "环境信息"
        verbose_name_plural = '环境信息'
        # 设置联合主键
        unique_together = [
            ('name', 'abs_name'),
        ]

    def __str__(self):
        return self.name


class System(models.Model):
    """
    系统信息
    """
    name = models.CharField(verbose_name="系统名", max_length=32)
    abs_name = models.CharField(verbose_name="系统名字简称", max_length=32)
    note = models.CharField(verbose_name="系统备注信息", max_length=255)
    # 一定要让系统有个维护人，不能没人维护呀。哈哈
    operate_person = models.ForeignKey(verbose_name="系统维护人",
                                       to=MyUser,
                                       on_delete=models.CASCADE,
                                       blank=False,
                                       null=False,
                                       related_name="system_operate_person")
    # 一个系统会有多个环境，一个环境中，会有多个系统，所以是多对多关系
    # 一个系统一定要属于一个环境，不能没有归属，流浪的环境哦
    environment = models.ManyToManyField(verbose_name="该系统拥有的环境",
                                         to=Environment,
                                         blank=False,
                                         related_name="system_environment"
                                         )
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "系统信息"
        verbose_name_plural = '系统信息'
        # 设置联合主键
        unique_together = [
            ('name', 'abs_name'),
        ]

    def __str__(self):
        return self.name


class Application(models.Model):
    """
    应用信息，存储中间件和java中的war包名，python中的项目名
    """
    middleware = models.CharField(verbose_name="中间件", max_length=32)
    name = models.CharField(verbose_name="应用名", max_length=32)
    note = models.CharField(verbose_name="备注信息", max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "应用信息"
        verbose_name_plural = "应用信息"
        # 设置联合主键
        unique_together = [
            ('middleware', 'name'),
        ]

    def __str__(self):
        return self.name


class HostLoginUser(models.Model):
    """
    登录虚拟机或服务器的用户信息，root或自己添加的普通用户
    """
    # 由于多个环境，多个系统，会出现登录用户相同，但是密码不同，所以这样设计了
    name_info = models.CharField(verbose_name="用户信息，建议system_environment_name", max_length=255)
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=2550)
    # upload_to上内置了strftime（）函数
    key_file = models.FileField(verbose_name="私钥文件",
                                upload_to='upload/privatekey/%Y%m%d/{}-{}'.
                                format(time.time(), random.randint(0, 99999)),
                                blank=True, null=True)
    # 这里是根据我之前的经验，为了密码安全，需要定期修改密码
    # 这里稍后我会做个定时任务，检查密码是否即将过期，提示用户
    expire_date = models.DateField(verbose_name="密码有效期", null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "主机登录用户信息"
        verbose_name_plural = "主机登录用户信息"
        # 设置联合主键
        unique_together = [
            ('name_info', 'name'),
        ]
        ordering = ["create_time"]

    def __str__(self):
        return "%s_%s" % (self.name_info, self.name)


class Host(models.Model):
    """
    主机信息
    """
    ip = models.CharField(verbose_name="主机IP", max_length=32, unique=True)
    note = models.CharField(verbose_name="备注信息", max_length=255)
    # 下面的信息可以通过点击按钮，进行异步获取
    MAC = models.CharField(verbose_name="物理MAC地址", max_length=32, blank=True, null=True)
    hostname = models.CharField(verbose_name="主机名", max_length=32, blank=True, null=True)
    cpu = models.IntegerField(verbose_name="CPU核数", blank=True, null=True)
    disk = models.IntegerField(verbose_name="磁盘大小，默认存的是KB", blank=True, null=True)
    mem = models.IntegerField(verbose_name="内存大小，默认存的是KB", blank=True, null=True)
    # 一定要让系统有个维护人，不能没人维护呀。哈哈
    operate_person = models.ForeignKey(verbose_name="主机维护人",
                                       to=MyUser,
                                       on_delete=models.CASCADE,
                                       blank=False,
                                       null=False,
                                       related_name="host_operate_person")
    # 一定是属于某个系统的，不能是放在那没啥用的
    system = models.ForeignKey(verbose_name="所属系统",
                               to=System,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False,
                               related_name="host_system")
    environment = models.ForeignKey(verbose_name="所属环境",
                                    to=Environment,
                                    on_delete=models.CASCADE,
                                    blank=False,
                                    null=False,
                                    related_name="host_environment")
    application = models.ManyToManyField(verbose_name="主机上安装的应用",
                                         to=Application,
                                         blank=False,
                                         related_name="host_application")
    login_user = models.ManyToManyField(verbose_name="主机的登录用户",
                                        to=HostLoginUser,
                                        blank=False,
                                        related_name="host_login_user")
    # 由于有些主机使用一段时间就不需要了，所以设置个有效期
    expire_date = models.DateTimeField(verbose_name="主机使用有效期", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "主机信息"
        verbose_name_plural = "主机信息"

    def __str__(self):
        return self.ip
