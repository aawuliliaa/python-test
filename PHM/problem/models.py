from django.db import models
from sign.models import UserInfo


class Problem(models.Model):
    """
    问题记录表
    """
    desc = models.CharField(verbose_name="问题描述", max_length=255)
    # 详情，使用kindeditor
    detail = models.TextField(verbose_name="详情")
    create_person = models.ForeignKey(verbose_name="问题提出人",
                                      to=UserInfo,
                                      on_delete=models.CASCADE,
                                      related_name="problem_create_person", blank=True, null=True)
    deal_person = models.ForeignKey(verbose_name="问题处理人",
                                    to=UserInfo,
                                    on_delete=models.CASCADE,
                                    related_name="problem_deal_person", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="问题创建时间", auto_now_add=True)
    start_deal_time = models.DateTimeField(verbose_name="问题开始处理时间", null=True, blank=True)
    stop_deal_time = models.DateTimeField(verbose_name="问题完成时间", null=True, blank=True)
    status_choices = (
        (1, '未处理'),
        (2, '处理中'),
        (3, '完成'),

    )
    status = models.IntegerField(verbose_name="状态", choices=status_choices)

    class Meta:
        verbose_name = "问题记录表"
        verbose_name_plural = '问题记录表'

    def __str__(self):
        return self.desc


class FollowUpRecord(models.Model):
    """
    跟进记录表
    """
    detail = models.TextField(verbose_name="详情")
    create_person = models.ForeignKey(verbose_name="问题跟进人",
                                      to=UserInfo,
                                      on_delete=models.CASCADE,
                                      related_name="follow_record_create_person", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    problem = models.ForeignKey(verbose_name="对应的问题",
                                to=Problem,
                                on_delete=models.CASCADE,
                                related_name="follow_record_problem", blank=True, null=True)

    class Meta:
        verbose_name = "问题记录表"
        verbose_name_plural = '问题记录表'
