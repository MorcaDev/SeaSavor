from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import api_form, api_json

urlpatterns = [
    path('api_form/', api_form, name="api_form"),
    path('api_json/', api_json, name="api_json"),
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
