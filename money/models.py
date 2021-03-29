from django.db import models

from django.contrib.auth.models import User

class TransactionType(models.Model):
    txn_type    = models.CharField(max_length=200)
    isAnExpense = models.CharField(max_length=5)
    
    def __str__(self):
        return self.txn_type
    

class Transaction(models.Model):
    transaction_name    = models.CharField(max_length=2000)
    transaction_summary = models.TextField()
    transaction_date    = models.DateTimeField(null=False)
    transaction_amount  = models.IntegerField(blank=True)
    transaction_type    = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    isInitialIncome     = models.CharField(max_length=3, blank=True)
    
    def __str__(self):
        return self.transaction_name
    
    
    
    
