from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .api import api
admin.autodiscover()



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
