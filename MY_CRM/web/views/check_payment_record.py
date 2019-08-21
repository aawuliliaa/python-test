#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url
from stark.service.v1 import StarkHandler, get_choice_text, get_datetime_text


class CheckPaymentRecordHandler(StarkHandler):

    order_list = ['-id','confirm_status']

    list_display = [StarkHandler.display_checkbox, 'customer', get_choice_text('缴费类型', 'pay_type'), 'paid_fee',
                    'class_list',
                    get_datetime_text('申请日期', 'apply_date'),
                    get_choice_text('状态', 'confirm_status'), 'consultant']

    def get_list_display(self):
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_urls(self):
        patterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            # url(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            # url(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
            # url(r'^delete/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    def action_multi_confirm(self, request, *args, **kwargs):
        """
        批量确认
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        # 缴费记录
        # 客户表
        # 学生表
        for pk in pk_list:
            payment_object = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payment_object:
                continue
            payment_object.confirm_status = 2
            payment_object.save()

            payment_object.customer.status = 1
            payment_object.customer.save()

            payment_object.customer.student.student_status = 2
            payment_object.customer.student.save()

    action_multi_confirm.text = '批量确认'

    def action_multi_cancel(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, confirm_status=1).update(confirm_status=3)

    action_multi_cancel.text = '批量驳回'

    action_list = [action_multi_confirm, action_multi_cancel]
