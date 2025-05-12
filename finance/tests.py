from django.test import TestCase, Client
from django.urls import reverse
from finance.models import Expense, Category
import json

class UpdateExpenseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Food')
        self.expense = Expense.objects.create(
            category=self.category,
            amount=150,
            date='2024-05-10',
            notes='Lunch'
        )
        self.url = f'/api/expenses/update/{self.expense.id}/'  # Match with your actual URL

    def test_update_expense_success(self):
        data = {
            "category": "Travel",
            "date": "2024-05-11"
        }
        response = self.client.put(self.url,
                                   data=json.dumps(data),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Updated')

        self.expense.refresh_from_db()
        self.assertEqual(self.expense.category, "Travel")
        self.assertEqual(str(self.expense.date), "2024-05-11")

    def test_update_expense_invalid_id(self):
        response = self.client.put('/api/expenses/update/999/',
                                   data=json.dumps({"category": "Misc"}),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_update_expense_invalid_json(self):
        response = self.client.put(self.url,
                                   data="not-a-json",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_update_expense_wrong_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)