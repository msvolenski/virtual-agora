from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agora'
urlpatterns = [
  url(r'^meuespacoartigo/$', views.MeuEspacoArtigoView.as_view(), name='meu-espaco-artigo'),
  url(r'^meuespacodebate/$', views.MeuEspacoDebateView.as_view(), name='meu-espaco-debate'),
  url(r'^meuespacoquestao/$', views.MeuEspacoQuestaoView.as_view(), name='meu-espaco-questao'),
  url(r'^meuespacooutros/$', views.MeuEspacoOutrosView.as_view(), name='meu-espaco-outros'),
  url(r'^meuespacoartigo/envia/$', views.enviaDadosMeuEspaco, name='envia-espaco-artigo'),
  url(r'^meuespacodebate/envia/$', views.enviaDadosMeuEspacoDebate, name='envia-espaco-debate'),
  url(r'^meuespacoquestao/envia/$', views.enviaDadosMeuEspacoQuestao, name='envia-espaco-questao'),
  url(r'^meuespacooutros/envia/$', views.enviaDadosMeuEspacoOutros, name='envia-espaco-outros'),
  url(r'^termo/$', views.TermoView.as_view(), name='termo'),
  url(r'^termo/accepted/$', views.term_accepted, name='term_accepted'),
  url(r'^termo/notaccepted/$', views.term_not_accepted, name='term_not_accepted'),
  url(r'^pdpu/home/$', views.HomeView.as_view(), name='home'),
  url(r'^pdpu/paginainicial/$', views.PdpuView.as_view(), name='pdpu'),
  url(r'^pdpu/participe/$', views.PdpuParticipeView.as_view(), name='pdpu-participe'),
  url(r'^pdpu/participe/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
  url(r'^pdpu/search/(?P<tag_name>\w+)/$', views.tag_search, name='search'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/voteiframe/$', views.vote_iframe, name='vote_iframe'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/voteinitial/$', views.vote_initial, name='vote_initial'),
  url(r'^pdpu/participe/(?P<question_id>[0-9]+)/votetimeline/$', views.vote_timeline, name='vote_timeline'),
]
