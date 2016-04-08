from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agora'
urlpatterns = [


  url(r'^participe/$', views.ParticipeView.as_view(), name='participe'),
  url(r'^participe/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
  url(r'^participe/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
  url(r'^participe/(?P<question_id>[0-9]+)/voteiframe/$', views.vote_iframe, name='vote_iframe'),
  url(r'^participe/(?P<question_id>[0-9]+)/voteinitial/$', views.vote_initial, name='vote_initial'),
  url(r'^participe/(?P<question_id>[0-9]+)/votetimeline/$', views.vote_timeline, name='vote_timeline'),
]
