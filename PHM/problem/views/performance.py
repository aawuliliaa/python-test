#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.views import View
import json
import datetime
from django.shortcuts import render
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from problem.views.chart_jsonresponse import JsonResponse
from problem.models import Problem
from problem.utils import dev_ops_user_dict
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./problem/templates/performance/templates/"))


def problem_count(user_id_list, problem_set):
    """
    返回每个人处理的问题数，放在列表中，用于图形展示
    :param user_id_list:
    :param problem_set:
    :return:
    """
    user_deal_problem_count_list = []
    ordered_dict = OrderedDict()

    for problem_obj in problem_set:
        deal_person_id = problem_obj.deal_person_id
        if deal_person_id not in ordered_dict:
            ordered_dict[deal_person_id] = 1
        else:
            ordered_dict[deal_person_id] += 1
    for user_id in user_id_list:
        user_deal_problem_count_list.append(ordered_dict.get(user_id))

    return user_deal_problem_count_list


class ProblemCountJsonView(View):
    """
    每人处理的问题数
    """
    def get(self, request, *args, **kwargs):
        dev_ops_user_id_name_dict = dev_ops_user_dict()
        user_id_list = dev_ops_user_id_name_dict.get("user_id_list")
        user_name_list = dev_ops_user_id_name_dict.get("user_name_list")
        problem_set = None
        title = None
        param = request.GET.get("date")
        if param == "today":
            title = "每人当日处理问题数"
            # 查询当天的数据
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__gte=datetime.datetime.now().date())
        elif param == "this_month":
            title = "每人当月处理问题数"
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__year=datetime.datetime.now().year,
                                                 create_time__month=datetime.datetime.now().month)
        elif param == "this_year":
            title = "每人本年处理问题数"
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__year=datetime.datetime.now().year)
        user_deal_problem_count_list = problem_count(user_id_list, problem_set)
        c = (
            Line()
            .add_xaxis(user_name_list)
            .add_yaxis(title, user_deal_problem_count_list)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=""))
            .dump_options()
        )
        return JsonResponse(json.loads(c))


class ProblemCountIndexView(View):
    """
    每人处理的问题数
    """
    def get(self, request, *args, **kwargs):
        return render(request, "./problem/problem_count_index.html")


def problem_deal_time(user_id_list, problem_set):
    """
    返回每个人处理问题的时间
    :param user_id_list:
    :param problem_set:
    :return:
    """
    user_deal_problem_time_list = []
    ordered_dict = OrderedDict()

    for problem_obj in problem_set:
        deal_person_id = problem_obj.deal_person_id
        start_deal_time = problem_obj.start_deal_time
        stop_deal_time = problem_obj.stop_deal_time if problem_obj.stop_deal_time is not None else datetime.datetime.now()
        deal_time = (stop_deal_time - start_deal_time).seconds/60
        if deal_person_id not in ordered_dict:
            ordered_dict[deal_person_id] = deal_time
        else:
            ordered_dict[deal_person_id] += deal_time
    for user_id in user_id_list:
        user_deal_problem_time_list.append(ordered_dict.get(user_id))
    return user_deal_problem_time_list


class ProblemDealTimeJsonView(View):
    """
    每人处理的问题时间
    """
    def get(self, request, *args, **kwargs):
        dev_ops_user_id_name_dict = dev_ops_user_dict()
        user_id_list = dev_ops_user_id_name_dict.get("user_id_list")
        user_name_list = dev_ops_user_id_name_dict.get("user_name_list")
        problem_set = None
        title = None
        param = request.GET.get("date")
        if param == "today":
            title = "每人当日处理问题时间(单位：分钟)"
            # 查询当天的数据
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__gte=datetime.datetime.now().date())
        elif param == "this_month":
            title = "每人当月处理问题时间(单位：分钟)"
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__year=datetime.datetime.now().year,
                                                 create_time__month=datetime.datetime.now().month)
        elif param == "this_year":
            title = "每人本年处理问题时间(单位：分钟)"
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__year=datetime.datetime.now().year)
        user_deal_problem_time_list = problem_deal_time(user_id_list, problem_set)
        c = (
            Line()
            .add_xaxis(user_name_list)
            .add_yaxis(title, user_deal_problem_time_list)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=""))
            .dump_options()
        )
        return JsonResponse(json.loads(c))


class ProblemDealTimeIndexView(View):
    """
    每人处理问题的时间
    """
    def get(self, request, *args, **kwargs):
        return render(request, "./problem/problem_deal_time_index.html")


def problem_efficient_time(user_id_list, problem_set):
    """
    每人处理的问题时效
    开始处理问题时间-create_time
    :param user_id_list:
    :param problem_set:
    :return:
    """
    user_problem_efficient_time_list = []
    ordered_dict = OrderedDict()

    for problem_obj in problem_set:
        deal_person_id = problem_obj.deal_person_id
        start_deal_time = problem_obj.start_deal_time
        create_time = problem_obj.create_time
        deal_time = (start_deal_time - create_time).seconds/60
        if deal_person_id not in ordered_dict:
            ordered_dict[deal_person_id] = deal_time
        else:
            ordered_dict[deal_person_id] += deal_time
    for user_id in user_id_list:
        user_problem_efficient_time_list.append(ordered_dict.get(user_id))
    return user_problem_efficient_time_list


class ProblemEfficientJsonView(View):
    """
    每人处理的问题时效
    """
    def get(self, request, *args, **kwargs):
        dev_ops_user_id_name_dict = dev_ops_user_dict()
        user_id_list = dev_ops_user_id_name_dict.get("user_id_list")
        user_name_list = dev_ops_user_id_name_dict.get("user_name_list")
        problem_set = None
        title = None
        param = request.GET.get("date")
        if param == "today":
            title = "每人当日处理问题时间(单位：分钟)"
            # 查询当天的数据
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__gte=datetime.datetime.now().date())
        elif param == "this_month":
            title = "每人当月处理问题时间(单位：分钟)"
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__year=datetime.datetime.now().year,
                                                 create_time__month=datetime.datetime.now().month)
        elif param == "this_year":
            title = "每人本年处理问题时间(单位：分钟)"
            problem_set = Problem.objects.filter(deal_person_id__in=user_id_list,
                                                 create_time__year=datetime.datetime.now().year)
        user_problem_efficient_time_list = problem_efficient_time(user_id_list, problem_set)
        c = (
            Line()
            .add_xaxis(user_name_list)
            .add_yaxis(title, user_problem_efficient_time_list)
            .set_global_opts(title_opts=opts.TitleOpts(title=title, subtitle=""))
            .dump_options()
        )
        return JsonResponse(json.loads(c))


class ProblemEfficientIndexView(View):
    """
   每人处理的问题时效
    """
    def get(self, request, *args, **kwargs):
        return render(request, "./problem/problem_efficient_time_index.html")

