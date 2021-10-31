# Generated by Django 3.2.4 on 2021-06-06 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210604_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='interested_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('date_int', models.DateTimeField(auto_now=True)),
                ('MerchantRequestID', models.CharField(default='notprovided', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('transaction_code', models.CharField(max_length=50)),
                ('pay_for', models.CharField(max_length=50)),
            ],
        ),
    ]
