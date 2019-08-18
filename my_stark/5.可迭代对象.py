#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
如何一个类中定义了__iter__方法且该方法返回一个迭代器，那么就称该类实例化的对象为可迭代对象（对象可以被循环）。

迭代器和生成器，生成器是一种特殊的迭代器。
"""


class SearchGroupRow(object):
    def __init__(self, queryset_or_tuple):
        """

        :param queryset_or_tuple: 组合搜索关联获取到的数据
        """
        self.queryset_or_tuple = queryset_or_tuple

    def __iter__(self):
        # return iter([11, 22, 33])
        yield 1
        yield 2
        yield 3


row = SearchGroupRow([11, 22, 33])

for item in row:
    print(item)
