#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.conf.urls import re_path
from rbac.views import menu, role, second_menu, permission, multi_config_permission
app_name = "rbac"
urlpatterns = [
    re_path(r'^role/list/$', role.RoleView.as_view(), name='role_list'),  # rbac:role_list
    re_path(r'^role/add/$', role.RoleAddView.as_view(), name='role_add'),  # rbac:role_add
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.RoleEditView.as_view(), name='role_edit'),  # rbac:role_edit
    re_path(r'^role/del/(?P<pk>\d+)/$', role.RoleDelView.as_view(), name='role_del'),  # rbac:role_del

    re_path(r'^menu/list/$', menu.MenuView.as_view(), name='menu_list'),
    re_path(r'^menu/add/$', menu.MenuAddView.as_view(), name='menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.MenuEditView.as_view(), name='menu_edit'),
    re_path(r'^menu/del/(?P<pk>\d+)/$', menu.MenuDelView.as_view(), name='menu_del'),
    re_path(r'^second/menu/add/(?P<menu_id>\d+)/$', second_menu.SecondMenuAddView.as_view(), name='second_menu_add'),
    re_path(r'^second/menu/edit/(?P<pk>\d+)/$', second_menu.SecondMenuEditView.as_view(), name='second_menu_edit'),
    re_path(r'^second/menu/del/(?P<pk>\d+)/$', second_menu.SecondMenuDelView.as_view(), name='second_menu_del'),
    re_path(r'^permission/add/(?P<second_menu_id>\d+)/$', permission.PermissionAddView.as_view(), name='permission_add'),
    re_path(r'^permission/edit/(?P<pk>\d+)/$', permission.PermissionEditView.as_view(), name='permission_edit'),
    re_path(r'^permission/del/(?P<pk>\d+)/$', permission.PermissionDelView.as_view(), name='permission_del'),
    re_path(r'^multi/permissions/$', multi_config_permission.multi_config_permission, name='multi_permissions'),
    re_path(r'^multi/permissions/del/(?P<pk>\d+)/$',
            multi_config_permission.multi_permissions_del, name='multi_permissions_del'),
    # re_path(r'^distribute/permissions/$', menu.distribute_permissions, name='distribute_permissions'),
]
