# Generated by Django 3.2.4 on 2021-07-04 05:42

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_item_date_scheduled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_scheduled',
            field=models.DateTimeField(default=user.models.item.return_date_time),
        ),
    ]