# -*- coding: utf-8 -*-

from celery.task import task
from celery import shared_task
# If you want to use Celery with a project already using these patterns extensively and you don’t have the time to refactor the existing code then you can consider specifying the names explicitly instead of relying on the automatic naming:
#
# @task(name='proj.tasks.add')
# def add(x, y):
#     return x + y
# 上面是官网的说明，如果不想去弄复杂的名称解析，就自己指定定义一个name
# 否则动不动就报Received unregistered task
# 自定义要执行的task任务
@shared_task(name="print")
def print():
    return 'hello celery and django...'