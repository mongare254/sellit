# Generated by Django 3.2.4 on 2021-06-07 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0002_auto_20210606_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='succesful_mpesa_payments',
            name='Paying_user',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='unsuccesful_mpesa_payments',
            name='Paid_item',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='unsuccesful_mpesa_payments',
            name='Paying_user',
            field=models.CharField(max_length=50),
        ),
    ]