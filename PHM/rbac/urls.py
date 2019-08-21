#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.conf.urls import re_path
from rbac.views import menu, role
app_name = "rbac"
urlpatterns = [
    re_path(r'^role/list/$', role.RoleView.as_view(), name='role_list'),  # rbac:role_list
    re_path(r'^role/add/$', role.RoleAddView.as_view(), name='role_add'),  # rbac:role_add
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.RoleEditView.as_view(), name='role_edit'),  # rbac:role_edit
    re_path(r'^role/del/(?P<pk>\d+)/$', role.RoleDelView.as_view(), name='role_del'),  # rbac:role_del
    #
    #
    # # re_path(r'^user/list/$', user.user_list, name='user_list'),
    # # re_path(r'^user/add/$', user.user_add, name='user_add'),
    # # re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    # # re_path(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    # # re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),
    #
    re_path(r'^menu/list/$', menu.MenuView.as_view(), name='menu_list'),
    re_path(r'^menu/add/$', menu.MenuAddView.as_view(), name='menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.MenuEditView.as_view(), name='menu_edit'),
    re_path(r'^menu/del/(?P<pk>\d+)/$', menu.MenuDelView.as_view(), name='menu_del'),
    # re_path(r'^second/menu/add/(?P<menu_id>\d+)$', menu.second_menu_add, name='second_menu_add'),
    # re_path(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    # re_path(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),
    # re_path(r'^permission/add/(?P<second_menu_id>\d+)/$', menu.permission_add, name='permission_add'),
    # re_path(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    # re_path(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),
    # re_path(r'^multi/permissions/$', menu.multi_permissions, name='multi_permissions'),
    # re_path(r'^multi/permissions/del/(?P<pk>\d+)/$', menu.multi_permissions_del, name='multi_permissions_del'),
    # re_path(r'^distribute/permissions/$', menu.distribute_permissions, name='distribute_permissions'),
]
