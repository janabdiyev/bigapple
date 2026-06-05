from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("menu.urls")),
]

# Serve media in both dev and prod
if settings.MEDIA_ROOT:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
