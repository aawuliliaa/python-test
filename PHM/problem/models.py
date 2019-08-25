from django.db import models
from sign.models import UserInfo


class Problem(models.Model):
    desc = models.CharField(verbose_name="问题描述", max_length=255)
    # 详情，使用kindeditor
    detail = models.TextField()
    create_person = models.ForeignKey(verbose_name="问题提出人",
                                      to=UserInfo,
                                      on_delete=models.CASCADE,
                                      related_name="problem_create_person")
    deal_person = models.ForeignKey(verbose_name="问题处理人",
                                    to=UserInfo,
                                    on_delete=models.CASCADE,
                                    related_name="problem_deal_person")
    create_time = models.DateTimeField(verbose_name="问题创建时间", auto_now_add=True)
    start_deal_time = models.DateTimeField(verbose_name="问题开始处理时间", null=True, blank=True)
    stop_deal_time = models.DateTimeField(verbose_name="问题完成时间", null=True, blank=True)
    status_choices = (
        (1, '未处理'),
        (2, '处理中'),
        (3, '完成'),

    )
    status = models.IntegerField(verbose_name="状态", choices=status_choices)
