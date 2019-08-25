#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django import forms


class StarkModelForm(forms.ModelForm):
    """
    给所有字段添加form-control样式
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
