# coding=utf-8

import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    question = models.CharField(max_length=128, default=None, null=True, blank=True)
    answer = models.CharField(max_length=128, default=None, null=True, blank=True)

    def __unicode__(self):
        return self.user.username


def create_userprofile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_userprofile, sender=User)


class Subject(models.Model):
    SUBJECT_TYPES = (
        ('Teach', u'文化'),
        ('Ritual', u'礼宾'),
    )

    CATEGORIES = (
        ('Subject', u'问题'),
        ('Option', u'选项'),
    )

    content = models.CharField(max_length=100, default=None)
    is_multi = models.BooleanField(default=False, blank=True)
    is_answer = models.BooleanField(default=False, blank=True)
    category = models.CharField(choices=CATEGORIES, max_length=50, null=True, blank=True)
    subject_type = models.CharField(choices=SUBJECT_TYPES, max_length=10, null=True, blank=True)
    subject_content = models.ForeignKey('self', related_name='options_content', null=True)
    date_added = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)   # 用于表示题目可用不可用

    @property
    def format_output(self):
        """
        具体题目的格式化输出
        :return:
        {
            "question": "这是题目",
            "question_id": "题目ID",
            "is_multi": "是否多选",
            "type": "这是类型"
            "options":
            [{
                "option_id": "选项ID",
                "content": "这是选项1",
                "is_answer": True
            },
            {
                "option_id": "选项ID",
                "content": "这是选项2",
                "is_answer": False
            },...]
        }
        """
        options = self.options_content.all()
        ret = {
            'question': self.content,
            'question_id': self.id,
            'is_multi': self.is_multi,
            'type': u'文化' if self.subject_type == 'Teach' else u'礼宾',
            'options': [{'option_id': o.id, 'content': o.content, 'is_answer': o.is_answer} for o in options],
        }
        return ret

    @classmethod
    def get_subjects(cls):
        return cls.objects.filter(category='Subject').order_by('-id')

    @classmethod
    def get_subject_options(cls):
        """
        获取所有题目的相关信息
        :return:
        [{
            "question": "这是题目",
            "question_id": "题目ID",
            "is_multi": "是否多选",
            "type": "这是类型"
            "options":
            [{
                "option_id": "选项ID",
                "content": "这是选项1",
                "is_answer": True
            },
            {
                "option_id": "选项ID",
                "content": "这是选项2",
                "is_answer": False
            },...]
        },...]

        """
        ret = []
        subjects = cls.objects.filter(category='Subject').order_by('-id')
        for s in subjects:
            question = s.format_output
            ret.append(question)
        return ret


class News(models.Model):
    """
        北洋礼仪新闻
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    creator = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())


class IndexPage(models.Model):
    """
        首页配置信息: 图片 + 文章
    """

    CATEGORY = (
        ('Image', u'图片'),
        ('News', u'新闻'),
    )

    category = models.CharField(choices=CATEGORY, max_length=10)
    image = models.CharField(max_length=100)
    news = models.ForeignKey(News)
    ranking = models.IntegerField()
