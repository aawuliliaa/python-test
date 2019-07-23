#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.forms import ModelForm
from django import forms
from asset.models import *


class EnvironmentForm(ModelForm):
    class Meta:
        model = Environment
        fields = "__all__"  # 对所有字段转换
        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'abs_name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
        }
        # <input type="text" name="name" class="form-control" maxlength="32" required id="id_name">
        # 前端已经根据models.py中的设置进行了设置，输入的时候会发现只能最多输入32个字符
        # error_messages = {
        #     'name': {'invalid': "name无效", "max_length": "太长了"},
        #     'abs_name': {'invalid': "name无效", },
        #     'note': {'invalid': "name无效", },
        #
        # }
