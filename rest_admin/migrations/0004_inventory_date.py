# Generated by Django 3.2.6 on 2021-09-08 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rest_admin', '0003_inventory_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='Date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]