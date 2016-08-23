from django.contrib import admin
from leafserver.models import UserProfile, Subject, Option

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Subject)
admin.site.register(Option)