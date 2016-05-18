from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agoraunicamp'
urlpatterns = [
  url(r'^$', views.AgoraView.as_view(), name='agora'),
  url(r'^mural/$', views.MuralView.as_view(), name='mural'),
  url(r'^encerratutorial/$', views.encerraTutorial, name='encerra_tutorial'),
  url(r'^refazertutorial/$', views.refazerTutorial, name='re_tutorial'),
  url(r'^login/$', auth_views.login, name='login'),
  url(r'^logout/$', auth_views.logout, {'next_page':'/login/'}, name='logout'),
  url(r'^search/(?P<tag_name>\w+)/$', views.tag_search, name='search'),
  url(r'^termo/$', views.TermoView.as_view(), name='termo'),
  url(r'^termo/accepted/$', views.term_accepted, name='term_accepted'),
  url(r'^termo/notaccepted/$', views.term_not_accepted, name='term_not_accepted'),
  url(r'^configuracao/$', views.AgoraConfiguracaoView.as_view(), name='configuracoes'),
  url(r'^configuracao/apelido/$', views.agoraconfiguracaoapelido, name='apelido-config'),
  url(r'^configuracao/apelido/remover/$', views.agoraconfiguracaoapelidoremove, name='apelido-remove'),
  url(r'^configuracao/email/$', views.agoraconfiguracaoemail, name='email-config'),
  url(r'^meuespacoartigo/$', views.MeuEspacoArtigoView.as_view(), name='meu-espaco-artigo'),
  url(r'^meuespacodebate/$', views.MeuEspacoDebateView.as_view(), name='meu-espaco-debate'),
  url(r'^meuespacoquestao/$', views.MeuEspacoQuestaoView.as_view(), name='meu-espaco-questao'),
  url(r'^meuespacooutros/$', views.MeuEspacoOutrosView.as_view(), name='meu-espaco-outros'),
  url(r'^meuespacoartigo/envia/$', views.enviaDadosMeuEspaco, name='envia-espaco-artigo'),
  url(r'^meuespacodebate/envia/$', views.enviaDadosMeuEspacoDebate, name='envia-espaco-debate'),
  url(r'^meuespacoquestao/envia/$', views.enviaDadosMeuEspacoQuestao, name='envia-espaco-questao'),
  url(r'^meuespacooutros/envia/$', views.enviaDadosMeuEspacoOutros, name='envia-espaco-outros'),
  url(r'^paginainicial/$', views.PaginaInicialView.as_view(), name='paginainicial'),
  url(r'^atprojeto/(?P<projeto_nome>[-\w]+)/$', views.atualizaProjeto, name='atualiza-projeto'),

  #url(r'pdpu/conheca/$', views.TemplatePDPUConhecaView.as_view(template_name="conheca/pdpu-conheca.html"), name='pdpu-conheca'),
  #url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/$', views.ArticlePageView.as_view(), name='article_page'),
]
