from django.shortcuts import render, HttpResponse
from django import forms
from app01 import models
from django.forms import formset_factory


class MultiPermissionForm(forms.Form):
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
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiUpdatePermissionForm(forms.Form):
    # 多加了一个id字段，用于修改该Id的数据
    id = forms.IntegerField(
        # 隐藏字段
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
        # 初始化单选框中的choices数据
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


def multi_add(request):
    """
    批量添加
    :param request:
    :return:
    """
    # extra=2生成多少个form表单
    formset_class = formset_factory(MultiPermissionForm, extra=2)

    if request.method == 'GET':
        # 实例化
        formset = formset_class()
        return render(request, 'multi_add.html', {'formset': formset})

    formset = formset_class(data=request.POST)
    # [form(字段，错误),form(字段，错误),]
    print("formset--------", formset)
    # formset是前端的html代码
    print("type(formset)--------", type(formset))
    # type(formset)-------- <class 'django.forms.formsets.MultiPermissionFormFormSet'>
    if formset.is_valid():
        flag = True
        post_row_list = formset.cleaned_data  # 检查formset中没有错误信息，则将用户提交的数据获取到。
        print("--------------", post_row_list)
        # [{'title': '11', 'url': '1211', 'name': '212', 'menu_id': '1', 'pid_id': ''}, {}]
        for i in range(0, formset.total_form_count()):
            row = post_row_list[i]
            # 如果为空，即前端改行没有填写数据
            if not row:
                continue
            try:
                # 如果联合唯一索引报错，能捕捉到报错信息，但是报错信息是一个字符串，没有携带字段，无法把报错信息添加到formset.errors中。所以没有使用create()
                # models.Permission.objects.create(**row)
                # print(e)  # UNIQUE constraint failed: app01_permission.name
                obj = models.Permission(**row)
                obj.validate_unique()  # 检查当前对象在数据库是否存在唯一的异常。
                obj.save()
            except Exception as e:
                # 这种方式报错信息携带字段，能够方便的把报错信息存储到formset.errors中
                print(e)  # {'name': ['具有 URL别名 的 Permission 已存在。']}
                formset.errors[i].update(e)
                # print("formset.errors--------------------------",formset.errors)
                # [{'name': ['具有 URL别名 的 Permission 已存在。']}, {}]
                flag = False
        if flag:
            return HttpResponse('提交成功')
        else:
            # 校验失败，显示报错信息
            return render(request, 'multi_add.html', {'formset': formset})
        # 校验失败，显示报错信息
    return render(request, 'multi_add.html', {'formset': formset})


def multi_edit(request):
    # extra=0因为默认为1，会多一行
    formset_class = formset_factory(MultiUpdatePermissionForm, extra=0)
    if request.method == 'GET':
        # initial = [{"id":2},{}]
        formset = formset_class(
            initial=models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id'))
        return render(request, 'multi_edit.html', {'formset': formset})

    formset = formset_class(data=request.POST)
    if formset.is_valid():
        post_row_list = formset.cleaned_data  # 检查formset中没有错误信息，则讲用户提交的数据获取到。
        flag = True
        for i in range(0, formset.total_form_count()):
            row = post_row_list[i]
            if not row:
                continue
            permission_id = row.pop('id')
            try:
                permission_object = models.Permission.objects.filter(id=permission_id).first()
                for key, value in row.items():
                    setattr(permission_object, key, value)
                permission_object.validate_unique()
                permission_object.save()

            except Exception as e:
                formset.errors[i].update(e)
                flag = False
        if flag:
            return HttpResponse('提交成功')
        else:
            return render(request, 'multi_edit.html', {'formset': formset})
    return render(request, 'multi_edit.html', {'formset': formset})
