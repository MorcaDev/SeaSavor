from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import form_api, rest_api

urlpatterns = [
    path('form_api/', form_api, name="form_api"),
    path('rest_api/', rest_api, name="rest_api"),
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
