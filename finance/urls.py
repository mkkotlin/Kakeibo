from django.contrib import admin
from django.urls import path

from finance.views import finance, expense_list, income_list



urlpatterns = [
    path('', finance, name = 'finance'),
    path('expenses/', expense_list, name = 'expense_list'),
    path('income/',income_list, name = 'income_list')
]