# juan_academy_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa settings per media files
from django.conf.urls.static import static # Importa static per servire media files

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Includi le URL dell'app 'core' alla root del sito
    path('accounts/', include('django.contrib.auth.urls')), # Per le URL di autenticazione predefinite di Django (login, logout, password reset, etc.)
]

# Serve i file media (immagini dei corsi, profile_pics, ecc.) solo in modalità DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Anche per i file statici se li gestisci così in sviluppo