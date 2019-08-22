#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django import forms
from rbac.models import Menu, Permission


class MultiAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-------------')],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '--------------')],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["menu_id"].choices += Menu.objects.values_list('id', 'title')
        self.fields["pid_id"].choices += Permission.objects.filter(pid__isnull=True, menu_id__isnull=False)\
            .values_list("id", "title")


class MultiEditPermissionForm(forms.Form):
    # 一定要设置id，这样修改的时候，才能根据Id进行修改
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,

    )

    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += Permission.objects.filter(pid__isnull=True, menu_id__isnull=False).\
            values_list('id', 'title')