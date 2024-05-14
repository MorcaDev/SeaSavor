from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('libro/', libro, name="libro"),
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
