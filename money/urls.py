from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.index_view, name='index'),
    path('addTransaction', views.addTransaction_view, name="addTransaction"),
    path('transactions', views.transactions_view, name="transactions"),
    path('transactionTypes',views.transactionTypes_view, name="transactionTypes"),
    path('',views.login_view, name="login"),
    path('register',views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('pie-chart',views.pie_chart_view, name="pieChart"),
    path('income_expense_chart',views.income_expense_chart, name="income_expense_chart"),
    path('initial_income',views.initial_income_view, name="initial_income"),
    
    
]