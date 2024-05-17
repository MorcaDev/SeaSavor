from django.urls import path
from .views import home, book

urlpatterns = [
    path('',home, name="home"),
    path('book/', book, name="book"),
]
