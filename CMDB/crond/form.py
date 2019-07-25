#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

from django import forms
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule


class CrontabScheduleForm(forms.ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = '__all__'
        widgets = {

            'minute': forms.TextInput(
                attrs={'class': 'form-control'}),
            'hour': forms.TextInput(
                attrs={'class': 'form-control'}),
            'day_of_week': forms.TextInput(
                attrs={'class': 'form-control'}),
            'day_of_month': forms.TextInput(
                attrs={'class': 'form-control'}),
            'month_of_year': forms.TextInput(
                attrs={'class': 'form-control'}),
        }
        help_texts = {
            "minute": "* 必填 任务名字",

        }



