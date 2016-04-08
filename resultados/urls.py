from django.conf.urls import url
from . import views
# -*- coding: utf-8 -*-

app_name = 'resultados'
urlpatterns = [
    url(r'^resultados/$', views.ResultadosView.as_view(template_name="resultados/resultados.html"), name='resultados'),
    url(r'^resultados/relatorio/(?P<pk>[0-9]+)/$', views.RelatorioPageView.as_view(), name='relatorio_page'),
    url(r'^resultados/relatorio/like/(?P<relatorio_id>[0-9]+)$', views.like, name='like'),
    url(r'^resultados/relatorio/dislike/(?P<relatorio_id>[0-9]+)$', views.dislike, name='dislike'),

]
