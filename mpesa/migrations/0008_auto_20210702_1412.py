# Generated by Django 3.2.4 on 2021-07-02 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0012_category_number'),
        ('mpesa', '0007_alter_mpesa_api_responses_the_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesa_api_responses',
            name='paid_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.item'),
        ),
        migrations.AlterField(
            model_name='mpesa_api_responses',
            name='the_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='succesful_mpesa_payments',
            name='Paid_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.item'),
        ),
        migrations.AlterField(
            model_name='succesful_mpesa_payments',
            name='Paying_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='unsuccesful_mpesa_payments',
            name='Paid_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.item'),
        ),
        migrations.AlterField(
            model_name='unsuccesful_mpesa_payments',
            name='Paying_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
