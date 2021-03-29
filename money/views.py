from django.shortcuts import render, redirect
from money.models import Transaction, TransactionType
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum
import datetime

# Create your views here.
def index_view(request):
    incomes   = getSumofAllIncomesByUser(request)
    expenses  = getSumOfAllExpensesByUser(request)
    remaining = incomes - expenses
    
    
    context = {
        'incomes':incomes,
        'expenses':expenses,
        'remaining':remaining,
        
    }
    return render(request, 'money/index.html', context)

def addTransaction_view(request):
    transaction_types = TransactionType.objects.all().exclude(txn_type="initial")
    if(request.method == "POST"):
        txn_name = request.POST["txn_name"]
        txn_summary = request.POST["txn_summary"]
        txn_amount = request.POST["txn_amount"]
        txn_type = TransactionType.objects.get(txn_type=request.POST["txn_type"])
        user = User.objects.get(username=request.user.username)
        
        transaction = Transaction.objects.create(
            transaction_name=txn_name,
            transaction_summary=txn_summary,
            transaction_date=datetime.datetime.now(),
            transaction_amount=txn_amount,
            transaction_type=txn_type,
            user = user
        )
        
        transaction.save()
        
        transactions = Transaction.objects.filter(transaction_type__isAnExpense="yes")
        txn_total = getSumOfAllExpenses()

        return render(request, 'money/transactionList.html', {'transactions':transactions, 'txn_total':txn_total, 'transaction_types':transaction_types })
    return render(request, 'money/addTransaction.html', {'transaction_types':transaction_types})

def getSumOfAllExpenses():
    total = Transaction.objects.filter(transaction_type__isAnExpense="yes").aggregate(Sum('transaction_amount'))
    txn_total = total["transaction_amount__sum"]
    return txn_total

def getSumOfAllExpensesByUser(request):  
     expenseList = Transaction.objects.filter(user__username=request.user.username).filter(transaction_type__isAnExpense="yes")
     if expenseList.exists():
        total = expenseList.aggregate(Sum('transaction_amount')) 
        txn_total = total["transaction_amount__sum"]   
     else:
         txn_total = 0
     return txn_total

def getSumofAllIncomesByUser(request):
     incomeList = Transaction.objects.filter(user__username=request.user.username).filter(transaction_type__isAnExpense="no")
     if incomeList.exists():
        total = incomeList.aggregate(Sum('transaction_amount')) 
        txn_total = total["transaction_amount__sum"]
     else:
        txn_total = 0
     print(txn_total)
     return txn_total

def getSumOfAllIncomes():
     total = Transaction.objects.filter(transaction_type__isAnExpense="no").aggregate(Sum('transaction_amount'))
     txn_total = total["transaction_amount__sum"]
     return txn_total
    

def addTransactionType_view(request):
    return render(request, "money/addTransactionTypes.html", {})

def transactions_view(request):
    # TOOO: make two tables for income and expense
    transactions = Transaction.objects.filter(user__username=request.user.username)
    incomeQuery = transactions.filter(transaction_type__isAnExpense="no")
    expenseQuery = transactions.filter(transaction_type__isAnExpense="yes")
    transaction_types = TransactionType.objects.all().exclude(txn_type="initial")
    expenseAmount = getSumOfAllExpensesByUser(request)
    incomeAmount = getSumofAllIncomesByUser(request)
    
    context = {
        'incomeQuery':incomeQuery,
        'expenseQuery':expenseQuery,
        'transaction_types':transaction_types,
        'expenseAmount':expenseAmount,
        'incomeAmount':incomeAmount,
    }
    if(request.method == "POST"):
        sortBytransactionTypes = request.POST["sortBytransactionTypes"]
        transactions = listQueriesByType(transactions, sortBytransactionTypes, request.user.username)
        total = Transaction.objects.filter(user__username=request.user.username).filter(transaction_type__txn_type=sortBytransactionTypes).aggregate(Sum('transaction_amount'))
        txn_total =  total["transaction_amount__sum"]

    return render(request, 'money/transactionList.html', context)

def listQueriesByType(transactions, sortBytransactionTypes, username):
    sortedTransactions = transactions.filter(user__username=username).filter(transaction_type__txn_type=sortBytransactionTypes)
    return sortedTransactions


def transactionTypes_view(request):
    if request.method == "POST":
        txn_type = request.POST["txn_type"]
        expenseType = request.POST["isAnExpense"]
        if expenseType == "income":
            isAnExpense = "no"
        else:
            isAnExpense = "yes"
        
        transaction_type = TransactionType.objects.create(txn_type=txn_type, isAnExpense=isAnExpense)
        transaction_type.save()
        return redirect('index')
    return render(request, 'money/addTransactionTypes.html', {})

def login_view(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                hasInitialIncome = Transaction.objects.filter(user__username=request.user.username).filter(isInitialIncome="yes")
                if hasInitialIncome.exists():
                    return redirect('index')
                else:
                    return redirect('initial_income')
            else:
                messages.info(request, "User is inactive")
        else:
            messages.info(request, "Email or password invalid")
    return render(request, 'money/login.html', {})

def initial_income_view(request):
    if(request.method == "POST"):
        txn_name = request.POST["txn_name"]
        txn_summary = request.POST["txn_summary"]
        txn_amount = request.POST["txn_amount"]
        try:
            txn_type = TransactionType.objects.get(txn_type="initial")
        except TransactionType.DoesNotExist:
            txn_type = TransactionType(txn_type="initial", isAnExpense="no")
            txn_type.save()

        user = User.objects.get(username=request.user.username)
        
        transaction = Transaction.objects.create(
            transaction_name=txn_name,
            transaction_summary=txn_summary,
            transaction_date=datetime.datetime.now(),
            transaction_amount=txn_amount,
            transaction_type=txn_type,
            user = user,
            isInitialIncome="yes",
        )
        
        transaction.save()
        return redirect('index')
        
    return render(request, 'money/initial_income.html', {})

def register_view(request):
    if(request.method == "POST"):
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        username = request.POST["username"]
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            
        elif User.objects.filter(email=email):
            messages.info(request, "Email is already registered")
        
        else:
            newUser = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_staff=True,
            )
            
            newUser.first_name = fname
            newUser.last_name = lname
            newUser.save()
            return redirect('login')
        
    return render(request, 'money/register.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

def pie_chart_view(request):
    labels = []
    data = []
    
    querySet = Transaction.objects.filter(user__username=request.user.username).order_by('-transaction_amount')[:5]
    for q in querySet:
        labels.append(q.transaction_name)
        data.append(q.transaction_amount)
        
    return JsonResponse(data={
        'labels':labels,
        'data':data,
    })
    
def income_expense_chart(request):
    labels = []
    data = []
    income_expense_queries = Transaction.objects.filter(user__username=request.user.username).values('transaction_type__isAnExpense').annotate(Sum('transaction_amount'))
    labels.append('expenses')
    labels.append('income')
    
    for q in income_expense_queries:
        data.append(q)
        
        print(q.transaction_amount)
    
    return JsonResponse(data={
        'labels':labels,
        'data':data,
    })
    
    
    
    
    
    
