from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authAPI.auth_urls')),
    path('user', include('authAPI.user_urls')),
    path('feed/', include('feedAPI.urls')),
    path('search/', include('searchAPI.urls')),
    path('push-alarm/', include('push_alarm.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
