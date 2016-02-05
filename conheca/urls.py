from django.conf.urls import url
from . import views
# -*- coding: utf-8 -*-

app_name = 'conheca'
urlpatterns = [
   
    url(r'pdpu/conheca/$', views.TemplatePDPUConhecaView.as_view(template_name="conheca/pdpu-conheca.html"), name='pdpu-conheca'),
    url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/$', views.ArticlePageView.as_view(), name='article_page'),
    url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/destaque/$', views.ArticleDestaquePageView.as_view(), name='article_page'),
    url(r'^pdpu/conheca/topicos/(?P<pk>[0-9]+)/$', views.TopicoPageView.as_view(), name='topico_page'),
    url(r'^pdpu/conheca/vote/$', views.search, name='search'),
     
]