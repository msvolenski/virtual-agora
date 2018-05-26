from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  url(r'^', include('django.contrib.auth.urls')), 
  url(r'^agora/', include('agoraunicamp.urls')),
  url(r'^admin/', admin.site.urls),
  url(r'^ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
