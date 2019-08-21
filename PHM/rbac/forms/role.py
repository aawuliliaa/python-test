#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from rbac.forms.base import BootStrapModelForm
from rbac import models


class RoleModelForm(BootStrapModelForm):
    class Meta:
        model = models.Role
        exclude = ['permissions']