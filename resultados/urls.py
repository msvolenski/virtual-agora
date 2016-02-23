from django.conf.urls import url
from . import views
# -*- coding: utf-8 -*-

app_name = 'resultados'
urlpatterns = [
   
    url(r'pdpu/resultados/$', views.TemplatePDPUResultadosView.as_view(template_name="resultados/pdpu-resultados.html"), name='pdpu-resultados'),
    url(r'^pdpu/resultados/relatorio/(?P<pk>[0-9]+)/$', views.RelatorioPageView.as_view(), name='relatorio_page'),
    #url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/destaque/$', views.ArticleDestaquePageView.as_view(), name='article_page'),
    #url(r'^pdpu/conheca/topicos/(?P<pk>[0-9]+)/$', views.TopicoPageView.as_view(), name='topico_page'),
    #url(r'^pdpu/conheca/vote/$', views.search, name='search'),
    url(r'^pdpu/resultados/relatorio/like/(?P<relatorio_id>[0-9]+)$', views.like, name='like'),
    url(r'^pdpu/resultados/relatorio/dislike/(?P<relatorio_id>[0-9]+)$', views.dislike, name='dislike'),
    url(r'^pdpu/resultados/relatorio/like/time/(?P<relatorio_id>[0-9]+)$', views.like_timeline, name='like_timeline'),
    url(r'^pdpu/resultados/relatorio/dislike/time/(?P<relatorio_id>[0-9]+)$', views.dislike_timeline, name='dislike_timeline'),
    url(r'^pdpu/resultados/search/$', views.search_res, name='search_res'),
                                              
     
]
