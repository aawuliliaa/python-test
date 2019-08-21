#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from rbac import models


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        # 只想修改，增加title字段，其余字段另做处理
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }

