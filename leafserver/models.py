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
	subject_choice = (
		'Teach',
		'Ritual',
	)

	context = models.CharField(max_length=100)
	is_multi = models.BooleanField(default=False)
	answer = models.IntegerField(default=0)
	choice = models.CharField(max_length=10)

	@property
	def get_options(self):
		return self.options

	def judge_answer(self, answer):
		answer = sum([int(a) for a in list(answer)])
		return answer == self.answer

	def __unicode__(self):
		return "%s.%s" % (self.id, self.context[:10])


class Option(models.Model):
	context = models.CharField(max_length=100)
	subject = models.ForeignKey(Subject, related_name='options')

	def __unicode__(self):
		return "%s -> %s.%s" % (self.context[:5], self.subject.id, self.subject.context[:10])
