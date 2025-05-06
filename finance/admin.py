from django.contrib import admin
from finance.models import Expense, Income

# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category','amount','date','notes')
    list_filter = ('category','date')
    search_fields = ('notes',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source','date','notes')
    list_filter = ('source','date')
    search_fields = ('source','notes')