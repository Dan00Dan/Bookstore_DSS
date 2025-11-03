"""
URL configuration for bookstore project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Cấu hình admin site
admin.site.site_header = "Quản trị cửa hàng sách"
admin.site.site_title = "Cửa hàng sách Admin"
admin.site.index_title = "Trang quản trị"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

