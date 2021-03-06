# Generated by Django 3.1.2 on 2021-03-22 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_type', models.CharField(max_length=200)),
                ('isAnExpense', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_name', models.CharField(max_length=2000)),
                ('transaction_summary', models.TextField()),
                ('transaction_date', models.DateTimeField()),
                ('transaction_amount', models.IntegerField(blank=True)),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.transactiontype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
