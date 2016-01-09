from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^agora/', include('agora.urls')),
    url(r'^admin/', admin.site.urls),
]