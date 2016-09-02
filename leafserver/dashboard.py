# coding=utf-8

import simplejson
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from functions import get_object_or_None, get_int
from models import IndexPage, Subject, News


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
        news = IndexPage.objects.filter(category='News').order_by('ranking')

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

        # 分页
        subjects = Subject.objects.filter(**filters).order_by('-date_added')[start: start + count + 1]
        next_start = -1
        if len(subjects) > count:
            next_start = start + count

        subjects = subjects[:count]
        s_list = []
        for s in subjects:
            s_list.append(s.format_output)

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
                若传入题目ID:
                {
                    'question': {
                        'content': '题目内容',
                        'is_multi': '是否多选',
                        'type': '题目类型',
                        'options': [{
                            'option_content': '这是选项',
                            'is_answer': '是否是答案',
                        },...]
                    }
                    'has_id': True
                    'question_types': (
                        ('Teach', u'文化'),
                        ('Ritual', u'礼宾'),
                    )
                }
                若未传入题目ID:
                {
                    'question': None,
                    'has_id': False
                    'question_types': (
                        ('Teach', u'文化'),
                        ('Ritual', u'礼宾'),
                    )
                }

        """
        q_id = get_int(request.GET.get('id', ''))
        ret = {
            'question': None,
            'has_id': False,
            'question_types': Subject.SUBJECT_TYPES,
        }
        question = get_object_or_None(Subject, pk=q_id)
        if question:
            ret['has_id'] = True
            ret['question'] = question.format_output

        return render(request, self.TEMPLATE, ret)

    def post(self, request):
        question = simplejson.loads(request.raw_post_data)
        subject = question['subject']
        options = question['options']

        # 若有ID信息 则是修改
        q_id = request.GET.get('id', '')

        # TODO: 返回信息
        code, msg = 0, ''

        if q_id:
            q_object = get_object_or_None(Subject, category='Subject', pk=q_id)
        else:
            q_object = Subject(category='Subjects')

        q_object.content = subject['content']
        q_object.is_multi = subject['is_multi']
        q_object.subject_type = subject['subject_type']
        q_object.save()

        # 题目选项修改 分成三部分
        # 1 修改前有ID的 修改后也有的 保存内容
        # 2 修改前有ID的 修改后没有的 删除信息
        # 3 修改前没有ID的 添加选项
        if q_id:
            old_options = q_object.options_content.all()
            old_o_ids = [old_o.id for old_o in old_options]
            new_o_ids = [new_o.get('id', '') for new_o in options]

            need_delete = list(set(old_o_ids) - set(new_o_ids))
            need_modify = list(set(old_o_ids) & set(new_o_ids))

            Subject.objects.filter(pk__in=need_delete).delete()
            for o_id in need_modify:
                option = Subject.objects.get(pk=o_id)
                for op in options:
                    if op['id'] == o_id:
                        option.content = op['content']
                        option.is_answer = bool(op['is_answer'])
                        break
                option.save()

            for op in options:
                if not op['id']:
                    option = Subject(category='Option')
                    option.content = op['content']
                    option.is_answer = bool(op['is_answer'])
                    option.subject_content = q_object
                    option.save()
        else:
            for op in options:
                option = Subject(category='Option')
                option.content = op['content']
                option.is_answer = bool(op['is_answer'])
                option.subject_content = q_object
                option.save()

        ret = {
            'code': code,
            'msg': msg,
        }
        return JsonResponse(ret)


class NewsEdit(View):
    TEMPLATE = 'dashboard/news_edit.html'

    @login_required()
    def get(self, request):
        n_id = request.GET.get('id', '')

        news = None
        if n_id:
            news = News.objects.get(pk=n_id)

        ret = {
            'news': news
        }

        return render(request, self.TEMPLATE, ret)

    @login_required()
    def post(self, request):
        n_id = request.GET.get('id', '')
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        user = request.user
        code, msg = 0, ''

        if n_id:
            news = News.objects.get(pk=n_id)
        else:
            news = News(creator=user)
        news.title = title
        news.content = content
        news.save()

        return JsonResponse({
            'code': code,
            'msg': msg,
        })
