from django.conf.urls import url

from . import views

app_name = 'forum'
urlpatterns = [
  # url(r'pdpu/comunidade/$', views.PdpuComunidadeView.as_view(), name='pdpu-comunidade'),
  url(r'^pdpu/forum/$', views.ForumHomeView.as_view(), name='home'),
  url(r'^pdpu/forum/(?P<slug>[-\w\d]+)&(?P<pk>[0-9]+)/$', views.ForumView.as_view(), name='forum'),
  url(r'^pdpu/forum/(?P<pk>[0-9]+)/$', views.TopicView.as_view(), name='topic'),
  url(r'^pdpu/forum/(?P<topic_id>[0-9]+)/answer/$', views.save_topic_answer, name='answer'),
  url(r'^pdpu/forum/(?P<topic_id>[0-9]+)/answerhome/$', views.save_topic_answer_home, name='answer_home'),
  # url(r'^pdpu/forum/categories/(?P<slug>[-\w\d]+)&(?P<pk>[0-9]+)/$', views.TopicView.as_view(), name='topic'),
  # url(r'pdpu/participe/$', views.PdpuParticipeView.as_view(), name='pdpu-participe'),
  # url(r'pdpu/resultados/$', views.PdpuResultadosView.as_view(), name='pdpu-resultados'),
  # url(r'pdpu/comunidade/$', views.PdpuComunidadeView.as_view(), name='pdpu-comunidade'),
  # url(r'^$', views.HomeView.as_view(), name='home'),
  # url(r'^pdpu/participe/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
  # url(r'^pdpu/participe/(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
  # url(r'^pdpu/participe/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
  # url(r'^posvotacao/$', views.posvotacao, name='posvotacao'),
]
