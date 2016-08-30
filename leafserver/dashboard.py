# coding=utf-8

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from leafserver.functions import get_object_or_None
from leafserver.models import IndexPage


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    def get(self, request):
        return render(request, self.TEMPLATE)


class HomeConfig(View):
    """
        配置首页: 轮播图片 + 新闻
    """
    TEMPLATE = 'dashboard/home_config.html'

    def get(self, request):

        images = IndexPage.objects.filter(category='Image').order_by('ranking')
        news   = IndexPage.objects.filter(category='News').order_by('ranking')

        ret = {
            'images': images,
            'news': news
        }
        return render(request, self.TEMPLATE, ret)

    def post(self, request):
        code, msg = 0, ''
        images = request.POST.getlist('images', [])
        news = request.POST.getlist('news', [])

        ret = {
            'code': code,
            'msg': msg
        }
        return JsonResponse(ret)


class QuestionsConfig(View):
    """
        配置答题: 题目 + 选项

        ==========
        请求方法:
            GET
        ==========
        请求参数:
            subject_type  |  N  |  题目类型
            start         |  N  |  开始位置
            count         |  N  |  条数
    """

    TEMPLATE = 'dashboard/question_config.html'

    def get(self, request):
        subject_type = request.GET.get('subject_type', '')

        return None
