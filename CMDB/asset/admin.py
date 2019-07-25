from django.contrib import admin
from asset.models import *


class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'abs_name', 'note', 'create_time', 'update_time']
    list_filter = ('name',)
    search_fields = ('name',)


class SystemAdmin(admin.ModelAdmin):
    # 不能列出多对多的字段
    list_display = ['name', 'abs_name', 'note', 'operate_person', 'create_time', 'update_time']
    list_filter = ('name',)
    search_fields = ('name',)
    # 多对多使用
    filter_horizontal = ('environment',)


class ApplicationAdmin(admin.ModelAdmin):
    # 不能列出多对多的字段
    list_display = ['middleware', 'name', 'note', 'create_time', 'update_time']
    list_filter = ('name',)
    search_fields = ('name',)


class HostLoginUserAdmin(admin.ModelAdmin):
    # 不能列出多对多的字段
    list_display = ['name_info', 'name', 'password', 'key_file', 'expire_date', 'create_time', 'update_time']
    list_filter = ('name', 'name_info')
    search_fields = ('name', 'name_info')


class HostAdmin(admin.ModelAdmin):
    # 不能列出多对多的字段
    list_display = ['ip', 'note', 'MAC', 'hostname', 'cpu', 'disk', 'mem', 'operate_person',
                    'system', 'environment', 'expire_date', 'create_time', 'update_time']
    list_filter = ('ip',)
    search_fields = ('ip',)
    # 多对多使用
    filter_horizontal = ('application', 'login_user')


admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(HostLoginUser, HostLoginUserAdmin)
admin.site.register(Host, HostAdmin)