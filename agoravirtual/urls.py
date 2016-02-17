from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
  url(r'^', include('django.contrib.auth.urls')),
  url(r'^agora/', include('agora.urls')),
  url(r'^agora/', include('forum.urls')),
  # url(r'^agora/', include('conheca.urls')),
  url(r'^admin/', admin.site.urls),
  url(r'^tinymce/', include('tinymce.urls')),
  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
