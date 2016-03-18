from django.contrib import admin

from .models import Category, Topic, TopicAnswer, Like


class TopicAdmin(admin.ModelAdmin):
  fields = ['category', 'title', 'text', 'tags']
  list_filter = ['pub_date']
  list_display = ['category', 'title', 'text', 'pub_date']


class TopicAnswerAdmin(admin.ModelAdmin):
  # fields = ['topic', 'text']
  list_filter = ['answer_date']
  list_display = ['user', 'topic', 'text', 'answer_date']


class LikeAdmin(admin.ModelAdmin):
  list_display = ['user', 'answer']


admin.site.register(Category)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicAnswer, TopicAnswerAdmin)
admin.site.register(Like, LikeAdmin)
