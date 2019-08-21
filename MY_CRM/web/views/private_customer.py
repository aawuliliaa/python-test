#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django.urls import reverse
from stark.service.v1 import StarkHandler, get_m2m_text, get_choice_text, StarkModelForm
from web import models

class PrivateCustomerModelForm(StarkModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', ]


class PrivateCustomerHandler(StarkHandler):
    model_form_class = PrivateCustomerModelForm

    def display_record(self, obj=None, is_header=None):
        if is_header:
            return '跟进记录'
        # 不需要保存原搜索条件，所以使用reverse
        record_url = reverse('stark:web_consultrecord_list', kwargs={'customer_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">跟进记录</a>' % record_url)
    def display_pay_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '缴费'
        record_url = reverse('stark:web_paymentrecord_list', kwargs={'customer_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">缴费</a>' % record_url)

    list_display = [StarkHandler.display_checkbox, 'name', 'qq', get_m2m_text('咨询课程', 'course'),
                    get_choice_text('状态', 'status'), display_record, display_pay_record]


    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            current_user_id = request.session['user_info']['id']
            form.instance.consultant_id = current_user_id
        form.save()

    def action_multi_remove(self, request, *args, **kwargs):
        """
        批量移除到公户
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, consultant_id=current_user_id).update(consultant=None)

    action_multi_remove.text = "移除到公户"

    action_list = [action_multi_remove]
