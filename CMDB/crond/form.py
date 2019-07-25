#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

from django import forms
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule


class CrontabScheduleForm(forms.ModelForm):
    """
    设置周期任务的form，
    """
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


class IntervalScheduleForm(forms.ModelForm):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'
        widgets = {

            'every': forms.TextInput(
                attrs={'class': 'form-control'}),
            'period': forms.Select(
                attrs={'class': 'form-control'}),
        }


class PeriodicTasksForm(forms.ModelForm):

    enabled = forms.BooleanField()

    class Meta:
        model = PeriodicTask
        fields = ['task', 'name', 'interval', 'crontab', 'args', 'kwargs', 'enabled', 'expires', 'description']

        widgets = {

            'task': forms.TextInput(
                attrs={'class': 'form-control'}),
            'name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'interval': forms.Select(
                attrs={'class': 'form-control'}),
            'crontab': forms.Select(
                attrs={'class': 'form-control'}),
            'args': forms.Textarea(
                attrs={'class': 'form-control'}),
            'kwargs': forms.Textarea(
                attrs={'class': 'form-control'}),

            'expires': forms.DateTimeInput(
                attrs={'type': 'date'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control'}),
        }