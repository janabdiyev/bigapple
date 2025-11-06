# urls.py (project level - bigapple/urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]

# Serve media files in both development AND production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
