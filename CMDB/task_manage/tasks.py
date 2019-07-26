# -*- coding: utf-8 -*-

from celery.task import task
from celery import shared_task,app

# 自定义要执行的task任务
# 一定要加上name,否则会报错Received unregistered task_manage
# 在我这个版本整体中，不能使用@app.task_manage
@shared_task(name="add")
def add(x,y):
    return x+y

