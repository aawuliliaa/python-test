# Generated by Django 2.2.3 on 2019-08-15 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_auto_20190815_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='pid',
            field=models.ForeignKey(blank=True, help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='rbac.Permission', verbose_name='关联的权限'),
        ),
    ]
