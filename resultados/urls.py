from django.conf.urls import url
from . import views
# -*- coding: utf-8 -*-

app_name = 'conheca'
urlpatterns = [
   
    url(r'pdpu/resultados/$', views.TemplatePDPUResultadosView.as_view(template_name="resultados/pdpu-resultados.html"), name='pdpu-resultados'),
    url(r'^pdpu/resultados/relatorio/(?P<pk>[0-9]+)/$', views.RelatorioPageView.as_view(), name='relatorio_page'),
    #url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/destaque/$', views.ArticleDestaquePageView.as_view(), name='article_page'),
    #url(r'^pdpu/conheca/topicos/(?P<pk>[0-9]+)/$', views.TopicoPageView.as_view(), name='topico_page'),
    #url(r'^pdpu/conheca/vote/$', views.search, name='search'),
     
]
