#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from web import models


class PaymentForm(ModelForm):
    class Meta:
        model = models.Payment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        self.fields['customer'].empty_label = "请选择客户"


class PaymentUserForm(ModelForm):
    class Meta:
        model = models.Payment
        exclude = ['customer',]

    def __init__(self, *args, **kwargs):
        super(PaymentUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
