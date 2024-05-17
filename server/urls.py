from django.urls import path

from .views import form_api, rest_api

urlpatterns = [
    path('form_api/', form_api, name="form_api"),
    path('rest_api/', rest_api, name="rest_api"),
]
