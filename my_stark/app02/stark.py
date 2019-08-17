#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse
from stark.service.v1 import site, StarkHandler
from app02 import models


class HostHandler(StarkHandler):
    pass


site.register(models.Host, HostHandler)

site.register(models.Role)

site.register(models.Project)
site.register(models.Project, prev='private')
