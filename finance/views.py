from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from finance.models import Expense, Income, Category
from django.core.serializers import serialize
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.


def finance(request):
    return HttpResponse("http://127.0.0.1:8000/api/income/  <br>    http://127.0.0.1:8000/api/expenses/")

@csrf_exempt
@require_http_methods(["GET","POST"])
def expense_list(request):
    if request.method == "GET":
        # data = Expense.objects.select_related('category').all()
        # result = [
        #     {
        #         "id":expense.id,
        #         "category":expense.category.name if expense.category else "Uncategorized",
        #         "amount":expense.amount,
        #         "date": expense.date,
        #         "notes":expense.notes
        #     }
        #     for expense in data
        # ]

# for filter
        category = request.GET.get('category')
        date = request.GET.get('date')
        expenses = Expense.objects.select_related('category').all()
        notes = request.GET.get('notes','').strip()
        

        if category:
            expenses = expenses.filter(category__name__iexact = category) #category==ForeignKey, __name== field inside Category, __iexact == case-insensitive and exact match
        if date:
            expenses = expenses.filter(date = date)
        if notes:
            expenses = expenses.filter(notes__icontains = notes)
        
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])


        min_amount = request.GET.get('min_amount')
        max_amount = request.GET.get('max_amount')
        try:
            if min_amount and max_amount:
                expenses = expenses.filter(amount__range=[min_amount, max_amount])
            elif min_amount:
                expenses = expenses.filter(amount__gte=min_amount)
            elif max_amount:
                expenses = expenses.filter(amount__lte=max_amount)
        except  ValueError:
            return JsonResponse({'error':'amount must be number'}, status=400)


        result = [
            {
                "id":expense.id,
                "category":expense.category.name if expense.category else "Uncategorized",
                "amount":expense.amount,
                "date": expense.date,
                "notes":expense.notes

            }
            for expense in expenses
        ]

        return JsonResponse(result, safe = False, json_dumps_params = {"indent":2})
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            category_id = data.get("category")
            category = Category.objects.get(id = category_id)
            expense = Expense.objects.create(
                category = category,
                # category = Category.objects.get(id = data.get("category")),
                amount = data.get('amount'),
                notes = data.get('notes', ''),
                date = data.get('date')
            )
            return JsonResponse({'message':'Expense created successfully', 'id': expense.id}, status=201)
        except Exception as e:
            # return JsonResponse({'error':str(e)}, status=400)
            return JsonResponse({'error':'Invalid category ID'},status = 400)

@csrf_exempt
@require_http_methods(["GET","POST"])
def income_list(request):
    if request.method == "GET":
        incomes = Income.objects.all()

# filters
        source = request.GET.get('source','').strip()
        if source:
            incomes = incomes.filter(source__icontains = source)
        min_amount = request.GET.get('min_amount')
        max_amount = request.GET.get('max_amount')
        try:
            if min_amount and max_amount:
                incomes = incomes.filter(amount__range=[min_amount,max_amount])
            elif min_amount:
                incomes = incomes.filter(amount__gte=min_amount)
            elif max_amount:
                incomes = incomes.filter(amount__lte=max_amount)
        except  ValueError:
            return JsonResponse({'error':'amount must be number'}, status=400)
        date = request.GET.get('date')
        if date:
            incomes = incomes.filter(date = date)
        notes = request.GET.get('notes')
        if notes:
            incomes = incomes.filter(notes__icontains = notes)

        result = [
            {
                "id":income.id,
                "source":income.source,
                "amount":income.amount,
                "date": income.date,
                "notes":income.notes
            }
            for income in incomes
        ]
        return JsonResponse(result, safe = False, json_dumps_params = {"indent":2})
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            income = Income.objects.create(
                source = data.get('source'),
                amount = data.get('amount'),
                notes = data.get('notes'),
            )
            return JsonResponse({'message':'income created successfully', 'id': income.id}, status=201)
        except Exception as e:
            return JsonResponse({'error':str(e)}, status=400)


@csrf_exempt
def delete_expense(request,expense_id):
    print(request,expense_id)
    if request.method == 'DELETE':
        try:
            expense = Expense.objects.get(id=expense_id)
            expense.delete()
            return JsonResponse({'message':'Deleted f"id {expense_id}"'},status = 200)
        except Expense.DoesNotExist:
            return JsonResponse({'error':'not found'}, status = 404)
    return JsonResponse({'error':'Invalid request'}, status = 400)


@csrf_exempt
def delete_income(request,income_id):
    print(request,income_id)
    if request.method == 'DELETE':
        try:
            expense = Income.objects.get(id=income_id)
            expense.delete()
            return JsonResponse({'message':'Deleted f"id {income_id}"'},status = 200)
        except Expense.DoesNotExist:
            return JsonResponse({'error':'not found'}, status = 404)
    return JsonResponse({'error':'Invalid request'}, status = 400)

@csrf_exempt
def UpdateExpense(request,pk):

    if request.method == 'PUT':
        try:
            expense = Expense.objects.get(id=pk)
        except Expense.DoesNotExist:
            return JsonResponse({'error':'Not Found'}, status = 404)
        try:
            data = json.loads(request.body.decode('utf-8'))
            expense.category = data.get('category',expense.category)
            expense.amount = data.get('amount',expense.amount)
            expense.date = data.get('date',expense.date)
            expense.notes = data.get('notes',expense.notes)
            expense.save()
            return JsonResponse({'message':'Updated'})
        except json.JSONDecodeError:
            return JsonResponse({'error':'invalid json'}, status = 400)
    return JsonResponse({'error':'Invalid Http method'}, status = 405)

@csrf_exempt
def UpdateIncome(request,pk):
    if request.method == 'PUT':
        try:
            income = Income.objects.get(id = pk)
        except Income.DoesNotExist:
            return JsonResponse({'error':'Not Found'}, status = 404)
        try:
            data = json.loads(request.body)
            income.source = data.get('source',income.source)
            income.amount = data.get('amount', income.amount)
            income.date = data.get('date', income.date)
            income.notes = data.get('notes',income.notes)
            income.save()
            return JsonResponse({'message':'Updated'})
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid json'}, status = 400)
    return JsonResponse({'error':'Invalid Http methos'}, status = 405)