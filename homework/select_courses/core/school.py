#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from core.db import SchoolDbHandler


class School:
    """
    用于创建学校对象
    """
    def __init__(self):
        self.school_name = None
        self.school_country = None
        self.school_city = None
        self.school_data = None

    def setter(self, school_name, school_country, school_city):
        """
        设置数据到学校对象中
        :param school_name:
        :param school_country:
        :param school_city:
        :return:
        """
        self.school_name = school_name
        self.school_country = school_country
        self.school_city = school_city
        return self

    def getter(self, school_name, school_data):
        """
        从文件中获取学校相关信息
        school_data {'school': <lib.schools.Schools object at 0x0000022CF265EFD0>,
                    'course': {'PY': <lib.courses.Courses object at 0x0000022CF266A208>},
                    'class': {'python': <lib.classes.Classes object at 0x0000022CF266A358>},
                    'teacher': {'vita': <lib.accounts.Accounts object at 0x0000022CF266A470>},
                    'student': {'lili': {'account_id': '777bbb7869ae8193249f8ff7d3e59afe',
                     'is_authenticated': True,
                     'account_data': <lib.accounts.StudentAccounts object at 0x0000022CF266A550>,
                     'student_data': {'school': 'SH', 'course': ['PY'],
                                     'class': ['python'],
                                     'teacher': ['vita']},
                                     'study_record': None}}}
        :param school_name:
        :param school_data:
        :return:
        """
        school_db_handler = SchoolDbHandler(school_name, school_data)
        self.school_data = school_db_handler.get_data_from_db()
        return self.school_data
