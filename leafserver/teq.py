# coding=utf-8

from django.views.generic import View


class TEQQuiz(View):
    TEMPLATE = 'teq/quiz.html'

    def get(self, request):
        """
        TEQ quiz 每次返回20题
        """
        QUIZ_COUNT = 20
        type = request.GET.get('type', '')
        
        return None


class TEQExam(View):
    TEMPLATE = 'teq/exam.html'

    def get(self, request):
        return None
