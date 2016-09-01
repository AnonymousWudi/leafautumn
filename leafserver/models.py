# coding=utf-8

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

    content = models.CharField(max_length=100)
    is_multi = models.BooleanField(default=False, None=True)
    is_answer = models.BooleanField(default=False, None=True)
    category = models.CharField(choices=CATEGORIES, max_length=50)
    subject_type = models.CharField(choices=SUBJECT_TYPES, max_length=10, null=True, blank=True)
    subject_content = models.ForeignKey('self', related_name='options_content', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_subjects(cls):
        return cls.objects.filter(category='Subject').order_by('-id')

    @classmethod
    def get_subject_options(cls):
        """
        :return:
        [{
            "question": "这是题目",
            "type": "这是类型"
            "options":
            [{
                "content": "这是选项1",
                "is_answer": True
            },
            {
                "content": "这是选项2",
                "is_answer": False
            },...]
        },...]

        """
        ret = []
        subjects = cls.objects.filter(category='Subject').order_by('-id')
        for s in subjects:
            options = s.options_content.all()
            question = {
                'question': s.content,
                'type': u'文化' if s.subject_type == 'Teach' else u'礼宾',
                'options': [{'content': o.content, 'is_answer': o.is_answer} for o in options],
            }
            ret.append(question)
        return ret


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


class News(models.Model):
    """
        北洋礼仪新闻
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
