#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import threading
import queue


class MyThread:
    """
        自定义的线程类，使用queue支持简单的线程池
    """
    def __init__(self, maxsize):
        """

        :param maxsize:  队列的数量
        """
        self.maxsize = maxsize
        self.q=queue.Queue(maxsize)  # 初始化一个队列对象
        # 在队列中先存放maxsize个队列对象。这一步就做到了线程池的作用。
        for i in range(maxsize):
            self.q.put(threading.Thread)  # 在队列中先存放线程对象

    def get_thread(self):
        """  从队列中拿取线程对象

        :return:
        """
        return self.q.get()

    def put_thread(self):
        """  往队列中存放线程对象

        :return:
        """
        self.q.put(threading.Thread)
