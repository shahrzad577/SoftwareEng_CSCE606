from django.contrib import admin

from .models import Question, feedbacks

admin.site.register(Question)
admin.site.register(feedbacks)
# Register your models here.
