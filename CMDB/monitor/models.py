from django.db import models
from asset.models import Host
from web.models import Role


class MonitorItem(models.Model):
    """
    监控项表
    """
    name = models.CharField(verbose_name="监控项名称", max_length=32)
    note = models.CharField(verbose_name="监控项介绍", max_length=255)
    monitor_script = models.CharField(verbose_name="获取监控数据的脚本", max_length=1000, blank=False, null=False)
    warn_expression = models.CharField(verbose_name="告警表达式", max_length=1000, blank=True, null=True)
    time_interval = models.CharField(verbose_name="时间间隔", max_length=32,blank=True, null=True)
    warn_type = models.CharField(verbose_name="告警方式", max_length=32, blank=False, null=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "监控项信息"
        verbose_name_plural = '监控项信息'
        # 设置联合主键
        unique_together = [
            ('name',),
        ]

    def __str__(self):
        return self.name


class Template(models.Model):
    """
    监控模板信息，与主机是多对多的关系
    """
    name = models.CharField(verbose_name="模板名称", max_length=32)
    note = models.CharField(verbose_name="模板介绍", max_length=255)
    notifier_role = models.ManyToManyField(verbose_name="告警通知角色",
                                           to=Role,
                                           blank=True,
                                           related_name="template_notifier_role")
    host = models.ManyToManyField(verbose_name="该模板关联的主机",
                                  to=Host,
                                  blank=True,
                                  related_name="template_host"
                                  )
    monitor_item = models.ManyToManyField(verbose_name="该模板关联的监控项",
                                          to=MonitorItem,
                                          blank=True,
                                          related_name="template_host"
                                          )
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "模板信息"
        verbose_name_plural = '模板信息'
        # 设置联合主键
        unique_together = [
            ('name', ),
        ]

    def __str__(self):
        return self.name


class WarnTable(models.Model):
    """
    告警表
    """
    name = models.CharField(verbose_name="监控项名称", max_length=32)
    get_data_time = models.DateTimeField(verbose_name="获取数据的时间")
    warn_expression = models.CharField(verbose_name="告警表达式", max_length=1000, blank=True, null=True)
    data = models.CharField(verbose_name="监控数据", max_length=32)
    ip = models.CharField(verbose_name="ip", max_length=32)

    class Meta:
        # db_table = "System" db_table是指定自定义数据库表名的。默认是appname_classname,可以这样自定义表名
        verbose_name = "告警信息"
        verbose_name_plural = '告警信息'

    def __str__(self):
        return self.name