from django.contrib import admin
from django.urls import path

from .views import finance



urlpatterns = [
    path('', finance, name = 'finance')
]