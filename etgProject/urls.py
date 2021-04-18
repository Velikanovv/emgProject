from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('frontend.urls')),
    path('staff/', include('staff.urls')),
    path('', include('users.urls')),
    path('', include('landing.urls')),
    path('api/v1/', include('api.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
