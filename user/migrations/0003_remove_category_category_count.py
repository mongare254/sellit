# Generated by Django 3.2.4 on 2021-06-04 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_category_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_count',
        ),
    ]