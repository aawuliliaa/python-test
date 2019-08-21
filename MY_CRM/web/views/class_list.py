#!/usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service.v1 import StarkHandler, get_datetime_text, get_m2m_text, StarkModelForm,Option
from stark.forms.widgets import DateTimePickerInput
from web import models
from django.urls import reverse
from django.utils.safestring import mark_safe
class ClassListModelForm(StarkModelForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput,
        }


class ClassListHandler(StarkHandler):

    def display_course(self, obj=None, is_header=None):
        if is_header:
            return '班级'
        return "%s %s期" % (obj.course.name, obj.semester,)

    def display_course_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '上课记录'
        record_url = reverse('stark:web_courserecord_list', kwargs={'class_id': obj.pk})
        return mark_safe('<a target="_blank" href="%s">上课记录</a>' % record_url)

    list_display = [
        'school',
        display_course,
        'price',
        get_datetime_text('开班日期', 'start_date'),
        'class_teacher',
        get_m2m_text('任课老师', 'tech_teachers'),
        display_course_record
    ]

    model_form_class = ClassListModelForm


    search_group = [
        Option('school'),
        Option('course'),
    ]