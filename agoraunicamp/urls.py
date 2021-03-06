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
  url(r'^post/curtir/(?P<proposta_pk>[-\w]+)/(?P<tipo>[-\w]+)$', views.curtir_proposta, name='curtir'),
  url(r'^meuespacoartigo/$', views.MeuEspacoArtigoView.as_view(), name='meu-espaco-artigo'),
  url(r'^meuespacodebate/$', views.MeuEspacoDebateView.as_view(), name='meu-espaco-debate'),
  url(r'^meuespacoquestao/$', views.MeuEspacoQuestaoView.as_view(), name='meu-espaco-questao'),
  url(r'^meuespacooutros/$', views.MeuEspacoOutrosView.as_view(), name='meu-espaco-outros'),
  url(r'^meuespacoartigo/envia/$', views.enviaDadosMeuEspaco, name='envia-espaco-artigo'),
  url(r'^meuespacodebate/envia/$', views.enviaDadosMeuEspacoDebate, name='envia-espaco-debate'),
  url(r'^meuespacoquestao/envia/$', views.enviaDadosMeuEspacoQuestao, name='envia-espaco-questao'),
  url(r'^meuespacooutros/envia/$', views.enviaDadosMeuEspacoOutros, name='envia-espaco-outros'),
  url(r'^paginainicial/$', views.PaginaInicialView.as_view(), name='paginainicial'),
  url(r'^configuracoes/enviafoto/$', views.simple_upload, name='simple-upload'),
  url(r'^atprojeto/(?P<projeto_nome>[\w ]+)/$', views.atualizaProjeto, name='atualiza-projeto'),
  url(r'^mudaetapa/(?P<etapa_nova>[-\w]+)/$', views.mudaEtapa, name='muda_etapa'),
  url(r'^forum/(?P<topic_id>[0-9]+)/answerhome/$', views.save_topic_answer_home, name='answer_home'),
  url(r'^forum/(?P<comment_id>[0-9]+)/answerreply/$', views.save_reply_answer_home, name='answer_reply'),
  url(r'^forum/(?P<reply_id>[0-9]+)/answerreplyedit/$', views.save_reply_answer_edit, name='answer_reply_edit'),
  url(r'^forum/(?P<comment_id>[0-9]+)/comment/delete/$', views.delete_comment, name='delete_comment'),
  url(r'^forum/(?P<reply_id>[0-9]+)/reply/delete/$', views.delete_reply, name='delete_reply'),
  url(r'^forum/(?P<topic_id>[0-9]+)/answerhomeedit/$', views.save_topic_answer_home_edit, name='answer_home_edit'),
  url(r'^participe/(?P<question_id>[0-9]+)/votetimeline/$', views.vote_timeline, name='vote_timeline'),
  url(r'^publicacao/(?P<projeto_nome>[\w ]+)/(?P<pub_id>[\w ]+)/$', views.carrega_publicacao, name='carrega_pbl'),
  
]
