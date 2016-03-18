from django.conf.urls import url
from . import views
# -*- coding: utf-8 -*-

app_name = 'resultados'
urlpatterns = [
    url(r'pdpu/resultados/$', views.TemplatePDPUResultadosView.as_view(template_name="resultados/pdpu-resultados.html"), name='pdpu-resultados'),
    url(r'^pdpu/resultados/relatorio/(?P<pk>[0-9]+)/$', views.RelatorioPageView.as_view(), name='relatorio_page'),
    url(r'^pdpu/resultados/relatorio/like/(?P<relatorio_id>[0-9]+)$', views.like, name='like'),
    url(r'^pdpu/resultados/relatorio/dislike/(?P<relatorio_id>[0-9]+)$', views.dislike, name='dislike'),
    url(r'^pdpu/resultados/relatorio/like/time/(?P<relatorio_id>[0-9]+)$', views.like_timeline, name='like_timeline'),
    url(r'^pdpu/resultados/relatorio/dislike/time/(?P<relatorio_id>[0-9]+)$', views.dislike_timeline, name='dislike_timeline'),
]
