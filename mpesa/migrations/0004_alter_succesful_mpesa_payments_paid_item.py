# Generated by Django 3.2.4 on 2021-06-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0003_auto_20210607_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='succesful_mpesa_payments',
            name='Paid_item',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
