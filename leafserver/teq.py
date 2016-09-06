# coding=utf-8

import random
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import Subject


class TEQQuiz(View):
    TEMPLATE = 'teq/quiz.html'

    @login_required()
    def get(self, request):
        """
        TEQ quiz 每次随机返回20题
        """
        QUIZ_COUNT = 20
        s_type = request.GET.get('type', 'Teach')     # 默认文化常识

        quiz_questions = Subject.get_subject_options(s_type=s_type)
        random.shuffle(quiz_questions)
        quiz_questions = quiz_questions[:QUIZ_COUNT]
        
        return render(request, self.TEMPLATE, quiz_questions)


class TEQExam(View):
    TEMPLATE = 'teq/exam.html'

    def get(self, request):
        return None
