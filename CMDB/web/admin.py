
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from web.models import *


# https://www.cnblogs.com/alex3714/articles/8997376.html详细说明参考
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin')
    list_display_links = ('email',)  # 点下这2个字段就跳到修改页
    list_per_page = 20 # 每页多少数据
    list_filter = ('is_admin',)
    # 这个是修改时，页面中有个分组
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # 创建用户时，列出的需要添加的字段信息
    add_fieldsets = (
        ("添加用户", {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    # 搜索字段
    search_fields = ('email', 'name')
    # 排序字段
    ordering = ('email',)
    # 多对多使用
    filter_horizontal = ()


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'parent_menu_name', 'child_menu_name', 'url', 'note', 'create_time', 'update_time']
    list_filter = ('name',)
    search_fields = ('name', 'code')
    filter_horizontal = ('users', 'privileges')
    list_display_links = ('id', 'name')  # 点下这2个字段就跳到修改页
    list_per_page = 20


class AccessLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'remote_ip', 'request_path', 'access_time']
    list_filter = ('remote_ip',)
    search_fields = ('remote_ip',)


class PrivilegeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'note', 'create_time', 'update_time']
    list_display_links = ('id', 'name')  # 点下这2个字段就跳到修改页
    list_per_page = 20
    list_filter = ('name',)
    search_fields = ('name',)


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(Privilege, PrivilegeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(AccessLog, AccessLogAdmin)

