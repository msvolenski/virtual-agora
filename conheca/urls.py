from django.conf.urls import url
from . import views
# -*- coding: utf-8 -*-

app_name = 'conheca'
urlpatterns = [
   
    url(r'pdpu/conheca/$', views.TemplatePDPUConhecaView.as_view(template_name="conheca/pdpu-conheca.html"), name='pdpu-conheca'),  
]