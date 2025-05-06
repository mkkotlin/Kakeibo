from django.db import models

# Create your models here.

# #
# class Category(models.Model):
#     name = models.CharField(max_length = 100, unique=True)

#     def __str__(self):
#         return self.name

class Expense(models.Model):
    
    CATEGORY_CHOICES = [
        ('food','Food'),
        ('transport','Transport'),
        ('bills','Bills'),
        ('entertainment','Entertainment'),
        ('health','Health'),
        ('others','Others'),
    ]

    category = models.CharField(max_length = 20, choices = CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField(auto_now_add = True)
    notes = models.TextField(blank = True)

    def __str__(self):
        return f"{self.category} - $ {self.amount} on {self.date}"

class Income(models.Model):
    source = models.CharField(max_length = 100)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField(auto_now_add = True)
    notes = models.TextField(blank = True)

    def __str__(self):
        return f"{self.source} - $ {self.amount} on {self.date}"
