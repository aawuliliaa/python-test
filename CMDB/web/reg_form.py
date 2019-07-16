
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from web.models import MyUser


class UserForm(forms.Form):
    # 用户form表单验证，主要功能在于进行字段的验证
    username = forms.CharField(label="用户名",
                               max_length=32,
                               error_messages={"required": "用户名不能为空"},
                               # 设置为input控件,并为其添加样式
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "Name"}))
    password = forms.CharField(label="密码",
                               min_length=3,
                               max_length=32,
                               error_messages={"required": "密码不能为空",
                                               "min_length": "密码不能少于3位",
                                               "max_length": "密码最长32位"},
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "Password"}))
    re_password = forms.CharField(label="确认密码",
                                  min_length=3,
                                  max_length=32,
                                  error_messages={"required": "密码不能为空",
                                                  "min_length": "密码不能少于3位",
                                                  "max_length": "密码最长32位"},
                                  widget=widgets.TextInput(attrs={"class": "form-control",
                                                                  "placeholder": "re_password"}))
    email = forms.EmailField(label="邮箱",
                             max_length=32,
                             error_messages={"required": "邮箱不能为空",
                                             "invalid": "邮箱格式错误"},
                             widget=widgets.EmailInput(attrs={"class": "form-control", "placeholder": "Email-@**.com"}))

    def clean_username(self):
        val = self.cleaned_data.get("username")
        user = MyUser.objects.filter(name=val).first()
        if user:

            raise ValidationError("该用户已经注册！")
        else:
            return val

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password and re_password:
            if password == re_password:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data
