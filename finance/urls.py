from django.contrib import admin
from django.urls import path

from finance.views import finance, expense_list, income_list, delete_expense, delete_income, UpdateExpense, UpdateIncome



urlpatterns = [
    path('', finance, name = 'finance'),
    path('api/expenses/', expense_list, name = 'expense_list'),
    path('api/income/',income_list, name = 'income_list'),
    path('api/expenses/<int:expense_id>/delete/', delete_expense, name = 'delete_expense'),
    path('api/income/<int:income_id>/delete/', delete_income, name = 'delete_income'),
    path('api/expenses/<int:pk>/update/',UpdateExpense, name = 'UpdateExpense'),
    path('api/income/<int:pk>/update/',UpdateIncome, name = 'UpdateIncome'),
]