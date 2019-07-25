from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule
from crond.form import *
from web.utils import return_show_data, get_label
from web.models import *


# 由于不需要自定义，就使用封装好的view啦，省事啦啦啦啦啦啦啦
class CrontabScheduleView(ListView):
    """
        定时任务时间 列表
        """

    template_name = 'crond/crontab_schedule.html'
    model = CrontabSchedule
    # context_object_name = "crontabs_list"
    queryset = CrontabSchedule.objects.all()
    ordering = ('-id',)

    def get_context_data(self, **kwargs):
        # 同样可以进行模糊查询
        data_page_info = return_show_data(self.request, self.queryset, *("minute",
                                                                         "hour",
                                                                         "day_of_week",
                                                                         "day_of_month",
                                                                         "month_of_year"))
        left_label_dic = get_label(self.request)
        role_obj = Role.objects.filter(url=self.request.path).first()
        context = {
            "data_page_info": data_page_info,
            "left_label_dic": left_label_dic,
            "role_obj": role_obj
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        """
        查询功能,先执行这个，在执行get_context_data。。看父类就知道了
        """
        self.queryset = super().get_queryset()

        return self.queryset


class AddCrontabSchedule(CreateView):
    """
    定时任务时间 增加
    """
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    queryset = CrontabSchedule.objects.all()
    template_name = 'crond/add_edit_crontab_schedule.html'
    success_url = reverse_lazy('crond:crontab_schedule')

    def get_context_data(self, **kwargs):
        left_label_dic = get_label(self.request)
        context = {
            "left_label_dic": left_label_dic
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DelCrontabSchedule(View):
    """
    删除环境信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        CrontabSchedule.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("crond:crontab_schedule"))


class IntervalScheduleView(ListView):
    """
        定时任务时间 列表
        """

    template_name = 'crond/interval_schedule.html'
    model = IntervalSchedule
    # context_object_name = "crontabs_list"
    queryset = IntervalSchedule.objects.all()
    ordering = ('-id',)

    def get_context_data(self, **kwargs):
        # 同样可以进行模糊查询
        data_page_info = return_show_data(self.request, self.queryset, *("every",
                                                                         "period",
                                                                         ))
        left_label_dic = get_label(self.request)
        role_obj = Role.objects.filter(url=self.request.path).first()
        context = {
            "data_page_info": data_page_info,
            "left_label_dic": left_label_dic,
            "role_obj": role_obj
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        """
        查询功能,先执行这个，在执行get_context_data。。看父类就知道了
        """
        self.queryset = super().get_queryset()

        return self.queryset


class AddIntervalSchedule(CreateView):
    """
    定时任务时间 增加
    """
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    queryset = IntervalSchedule.objects.all()
    template_name = 'crond/add_edit_interval_schedule.html'
    success_url = reverse_lazy('crond:interval_schedule')

    def get_context_data(self, **kwargs):
        left_label_dic = get_label(self.request)
        context = {
            "left_label_dic": left_label_dic
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DelIntervalSchedule(View):
    """
    删除环境信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        IntervalSchedule.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("crond:interval_schedule"))


class PeriodicTasksView(ListView):
    """
        定时任务时间 列表
        """

    template_name = 'crond/periodic_task.html'
    model = PeriodicTask
    # context_object_name = "crontabs_list"
    queryset = PeriodicTask.objects.all()
    ordering = ('-id',)

    def get_context_data(self, **kwargs):
        # 同样可以进行模糊查询
        data_page_info = return_show_data(self.request, self.queryset, *("name", "task"))
        left_label_dic = get_label(self.request)
        role_obj = Role.objects.filter(url=self.request.path).first()
        context = {
            "data_page_info": data_page_info,
            "left_label_dic": left_label_dic,
            "role_obj": role_obj
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        """
        查询功能,先执行这个，在执行get_context_data。。看父类就知道了
        """
        self.queryset = super().get_queryset()

        return self.queryset


class AddPeriodicTasks(CreateView):
    """
    定时任务时间 增加
    """
    model = PeriodicTask
    form_class = PeriodicTasksForm
    queryset = PeriodicTask.objects.all()
    template_name = 'crond/add_edit_periodic_task.html'
    success_url = reverse_lazy('crond:periodic_tasks')

    def get_context_data(self, **kwargs):
        left_label_dic = get_label(self.request)
        context = {
            "left_label_dic": left_label_dic
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DelPeriodicTasks(View):
    """
    删除环境信息
    """
    def get(self, request, **kwargs):
        # print("================2",kwargs)  #{'pk': 205}
        PeriodicTask.objects.filter(id=kwargs.get("pk")).delete()
        return redirect(reverse("crond:periodic_tasks"))


class EditPeriodicTasks(UpdateView):
    """
    周期任务 更新
    """

    model = PeriodicTask
    form_class = PeriodicTasksForm
    template_name = 'crond/add_edit_periodic_task.html'
    success_url = reverse_lazy('crond:periodic_tasks')

    def get_context_data(self, **kwargs):
        left_label_dic = get_label(self.request)
        context = {
            "left_label_dic": left_label_dic
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)