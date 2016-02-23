from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'agora'
urlpatterns = [
  url(r'^$', views.HomeView.as_view(), name='home'),
  url(r'^pdpu/$', views.PdpuView.as_view(), name='pdpu'),
  url(r'^login/$', auth_views.login, name='login'),
  url(r'^login/$', auth_views.logout, name='logout'),
  url(r'^pdpu/participe/$', views.PdpuParticipeView.as_view(), name='pdpu-participe'),
  url(r'^pdpu/participe/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/voteiframe/$', views.vote_iframe, name='vote_iframe'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/voteinitial/$', views.vote_initial, name='vote_initial'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/votetimeline/$', views.vote_timeline, name='vote_timeline'),
  url(r'^posvotacao/$', views.posvotacao, name='posvotacao'),
]
