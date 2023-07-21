from django.urls import path
from .views import kombat

urlpatterns = [
    path("kombat", kombat, name="kombat"),
]