from django.conf.urls import url

from . import views

app_name = 'forum'
urlpatterns = [
  url(r'^pdpu/forum/$', views.ForumHomeView.as_view(), name='home'),
  url(r'^pdpu/forum/(?P<slug>[-\w\d]+)&(?P<pk>[0-9]+)/$', views.ForumView.as_view(), name='forum'),
  url(r'^pdpu/forum/(?P<pk>[0-9]+)/$', views.TopicView.as_view(), name='topic'),
  url(r'^pdpu/forum/(?P<topic_id>[0-9]+)/answer/$', views.save_topic_answer, name='answer'),
  url(r'^pdpu/forum/(?P<topic_id>[0-9]+)/answerhome/$', views.save_topic_answer_home, name='answer_home'),
  url(r'^pdpu/forum/(?P<topic_id>[0-9]+)/answerhomeedit/$', views.save_topic_answer_home_edit, name='answer_home_edit'),
]
