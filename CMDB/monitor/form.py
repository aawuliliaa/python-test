#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.forms import ModelForm
from django import forms
from monitor.models import *


class TemplateForm(ModelForm):
    """
    环境信息form
    """
    class Meta:
        model = Template
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
            'notifier_role': forms.SelectMultiple(
                attrs={'class': 'form-control'}),
            'host': forms.SelectMultiple(
                attrs={'class': 'form-control'}),
            'monitor_item': forms.SelectMultiple(
                attrs={'class': 'form-control'}),
        }


class MonitorItemForm(ModelForm):
    """
    环境信息form
    """
    class Meta:
        model = MonitorItem
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
            'monitor_script': forms.Textarea(
                attrs={'class': 'form-control'}),
            'warn_expression': forms.TextInput(
                attrs={'class': 'form-control'}),
            'time_interval': forms.TextInput(
                attrs={'class': 'form-control'}),
            'warn_type': forms.TextInput(
                attrs={'class': 'form-control'}),
        }