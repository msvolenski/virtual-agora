from django.conf.urls import url

from . import views



app_name = 'agora'
urlpatterns = [
    url(r'pdpu/$', views.PdpuView.as_view(), name='pdpu'),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'agora/login-certo.html'} , name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'agora/login-certo.html'} ,name='logout'),
    #url(r'pdpu/conheca/$', views.TemplatePDPUConhecaView.as_view(template_name="agora/pdpu-conheca.html"), name='pdpu-conheca'),
    url(r'pdpu/participe/$', views.PdpuParticipeView.as_view(), name='pdpu-participe'),
    url(r'pdpu/resultados/$', views.PdpuResultadosView.as_view(), name='pdpu-resultados'),
    url(r'pdpu/comunidade/$', views.PdpuComunidadeView.as_view(), name='pdpu-comunidade'),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^pdpu/participe/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^pdpu/participe/(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^pdpu/participe/(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^posvotacao/$', views.posvotacao, name='posvotacao'),

]
