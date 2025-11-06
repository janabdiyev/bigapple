# bigapple/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]

# Serve media files in BOTH development and production
# This works regardless of DEBUG setting
if settings.MEDIA_ROOT:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]

# Also keep the static() helper for static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
