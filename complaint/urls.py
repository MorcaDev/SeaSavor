from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('book/', book, name="book"),
    path('api_form/', api_form, name="api_form"),
    path('api_json/', api_json, name="api_json"),
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
