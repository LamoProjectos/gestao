from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', core_views.service_worker, name='service_worker'),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('crm/', include('crm.urls')),
    path('projects/', include('projects.urls')),
    path('financial/', include('financial.urls')),
    path('documents/', include('documents.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
