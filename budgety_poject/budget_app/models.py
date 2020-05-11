from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class ExpenseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    expense_name = models.CharField(max_length=20)
    cost = models.DecimalField(decimal_places=2, max_digits=1_000_000_000)
    date_added = models.DateField()
    user_expense = models.ForeignKey(User, on_delete=models.CASCADE)
