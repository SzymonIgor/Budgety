from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import ExpenseInfo
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
from django.contrib import messages
from django.db.models import Q
# Create your views here.


@login_required(login_url='/')
def index(request):
    expense_items = ExpenseInfo.objects.filter(user_expense=request.user).order_by('-date_added')
    try:
        income_total = ExpenseInfo.objects.filter(user_expense=request.user).\
            aggregate(income=Sum('cost', filter=Q(cost__gt=0)))
        expense_total = ExpenseInfo.objects.filter(user_expense=request.user).\
            aggregate(expenses=Sum('cost', filter=Q(cost__lt=0)))

    except TypeError:
        print('No data.')
    expenses = round(abs(expense_total['expenses']) if expense_total['expenses'] is not None else 0, 2)
    income = round(abs(income_total['income']) if income_total['income'] is not None else 0, 2)
    budget_current = round(income - expenses, 2)
    fig, ax = plt.subplots()
    ax.bar(['expenses', 'income'], [expenses, income], color=['#FF5049', '#28B9B5'])
    ax.set_title('Your total expenses vs. total income')
    plt.savefig('budget_app/static/expense.png')
    try:
        expenses_prc = round(expenses/income * 100, 2)
    except:
        expenses_prc = 0
    context = {'expense_items':expense_items, 'income':income,'expenses': expenses, 'budget_current': budget_current,
               'expenses_prc':expenses_prc}
    return render(request, 'budget_app/index.html', context=context)


@login_required(login_url='/')
def add_item(request):
    try:
        name = request.POST['expense_name']
        expense_cost = request.POST['cost']
        date_added = request.POST['date_added']
        ExpenseInfo.objects.create(expense_name=name, cost=expense_cost, date_added=date_added,
                                   user_expense=request.user)
    except:
        messages.error(request, "Please fill up all of the fields below to add an item")
    return HttpResponseRedirect('app')


@login_required(login_url='/')
def del_item(request):
    id = request.POST['id']
    ExpenseInfo.objects.filter(id=id).delete()
    return HttpResponseRedirect('app')


@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('app')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    else:
        form = UserCreationForm
        return render(request, 'budget_app/sign_up.html', {'form': form})
