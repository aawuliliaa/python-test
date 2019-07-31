
from celery import shared_task

import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from celery import shared_task

@shared_task(name="tailf")
def tailf(id, channel_name):
    channel_layer = get_channel_layer()
    filename = settings.LOG_PATH[int(id)]
    print("llllllllllllllllllll")
    try:
        with open(filename) as f:
            # f.seek(0, 2)
            # 一开始任务总是不执行，才print调试
            # print("kkkkkkkkkk")
            while True:
                # print("dddd")
                line = f.readline()
                # print("ssssssssssss",line)
                if line:
                    print(".............",line)
                    print(channel_name, line)
                    async_to_sync(channel_layer.send)(
                        channel_name,
                        {
                            "type": "send.message",
                            "message": str(line)
                        }
                    )
                else:
                    time.sleep(0.5)
    except Exception as e:
        print(e)

@shared_task(name="add")
def add(x,y):
    print("add")
    return x+y