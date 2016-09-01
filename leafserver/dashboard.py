# coding=utf-8

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from functions import get_object_or_None, get_int
from models import IndexPage, Subject


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
        ==========
        返回格式:
            [{
                'question': '这是题目',
                'is_multi': '是否多选',
                'type': '题目类型',
                'options': [{
                    'option_content': '这是选项',
                    'is_answer': '是否是答案',
                },...]
            },...]
    """

    TEMPLATE = 'dashboard/question_config.html'

    def get(self, request):
        subject_type = request.GET.get('type', '')
        start = get_int(request.GET.get('start', ''))
        count = get_int(request.GET.get('count', '20'))

        filters = {
            'category': 'Subject',
            'is_active': True
        }
        if subject_type:
            filters['subject_type'] = subject_type

        subjects = Subject.objects.filter(**filters).order_by('-date_added')[start: start + count + 1]
        next_start = -1
        if len(subjects) > count:
            next_start = start + count

        subjects = subjects[:count]
        s_list = []
        for s in subjects:
            s_options = s.options_content.all()
            s_list.append({
                'question': s.content,
                'is_multi': s.is_multi,
                'type': s.subject_type,
                'options': [{'option_content': o.content, 'is_answer': o.is_answer} for o in s_options],
            })

        ret = {
            'next_start': next_start,
            'subjects': s_list,
        }

        return render(request, self.TEMPLATE, ret)


class QuestionEdit(View):
    TEMPLATE = 'dashboard/question_edit.html'

    def get(self, request):
        """
            添加题目 / 修改题目
            ==========
            请求方法:
                GET
            ==========
            请求参数:
                id  |  N  |  题目ID
            ==========
            返回格式:

        """
        q_id = get_int(request.GET.get('id', ''))


        return None
