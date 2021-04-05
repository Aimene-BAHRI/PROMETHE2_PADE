from django.contrib import admin
from django.urls import path, include
from .views import dashboard, send_matrix_to_all_dec, classification

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profile/', dashboard, name='user_dashboard'),
    path('send_mp/', send_matrix_to_all_dec, name='sendmp'),
    path('classification/', classification, name='classification')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
