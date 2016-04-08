from django.conf.urls import url
from . import views

app_name = 'conheca'
urlpatterns = [
  url(r'conheca/$', views.ConhecaView.as_view(template_name="conheca/conheca.html"), name='conheca'),
  url(r'^conheca/artigos/(?P<pk>[0-9]+)/$', views.ArticlePageView.as_view(), name='article_page'),
]
