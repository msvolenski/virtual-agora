from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agoraunicamp'
urlpatterns = [
  url(r'^$', views.AgoraView.as_view(), name='agora'),
  url(r'^login/$', auth_views.login, name='login'),
  url(r'^logout/$', auth_views.logout, {'next_page':'/login/'}, name='logout'),
  url(r'^termo/$', views.TermoView.as_view(), name='termo'),
  url(r'^termo/accepted/$', views.term_accepted, name='term_accepted'),
  url(r'^termo/notaccepted/$', views.term_not_accepted, name='term_not_accepted'),
  url(r'^configuracao/$', views.AgoraConfiguracaoView.as_view(), name='configuracoes'),
  url(r'^configuracao/apelido/$', views.agoraconfiguracaoapelido, name='apelido-config'),
  url(r'^configuracao/apelido/remover/$', views.agoraconfiguracaoapelidoremove, name='apelido-remove'),
  url(r'^configuracao/email/$', views.agoraconfiguracaoemail, name='email-config'),
  #url(r'pdpu/conheca/$', views.TemplatePDPUConhecaView.as_view(template_name="conheca/pdpu-conheca.html"), name='pdpu-conheca'),
  #url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/$', views.ArticlePageView.as_view(), name='article_page'),
]
