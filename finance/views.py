from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from finance.models import Expense, Income
from django.core.serializers import serialize
import json

# Create your views here.


def finance(request):
    return HttpResponse("http://127.0.0.1:8000/api/income/  <br>    http://127.0.0.1:8000/api/expenses/")


def expense_list(request):
    data = Expense.objects.select_related('category').all()
    result = [
        {
            "id":expense.id,
            "category":expense.category.name if expense.category else "Uncategorized",
            "amount":expense.amount,
            "date": expense.date,
            "notes":expense.notes
        }
        for expense in data
    ]
    return JsonResponse(result, safe = False, json_dumps_params = {"indent":2})



def income_list(request):
    data = Income.objects.all()
    result = [
        {
            "id":income.id,
            "source":income.source,
            "amount":income.amount,
            "data": income.date,
            "notes":income.notes
        }
        for income in data
    ]
    return JsonResponse(result, safe = False, json_dumps_params = {"indent":2})