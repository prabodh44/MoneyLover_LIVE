from django.contrib import admin
from money.models import TransactionType, Transaction

# Register your models here.
admin.site.register(Transaction)
admin.site.register(TransactionType)
