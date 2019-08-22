#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rbac import models
from rbac.forms.base import BootStrapModelForm


class SecondMenuModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        # fields = ['title', 'name', 'url']
        exclude = ['pid']



class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']

#
# class MultiAddPermissionForm(forms.Form):
#     title = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     url = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     name = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     menu_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#
#     )
#
#     pid_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
#         self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
#             menu__isnull=True).values_list('id', 'title')
#
#
# class MultiEditPermissionForm(forms.Form):
#     id = forms.IntegerField(
#         widget=forms.HiddenInput()
#     )
#
#     title = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     url = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     name = forms.CharField(
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     menu_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#
#     )
#
#     pid_id = forms.ChoiceField(
#         choices=[(None, '-----')],
#         widget=forms.Select(attrs={'class': "form-control"}),
#         required=False,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
#         self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
#             menu__isnull=True).values_list('id', 'title')
