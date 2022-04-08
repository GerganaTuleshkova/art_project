from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from art_project.accounts import signals

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('art_project.accounts.urls')),
                  path('', include('art_project.art_portal_app.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

