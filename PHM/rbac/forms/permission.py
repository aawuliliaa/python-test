#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from rbac import models
from rbac.forms.base import BootStrapModelForm


class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']