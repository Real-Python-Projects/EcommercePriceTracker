# Generated by Django 3.1.7 on 2021-04-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0014_auto_20210422_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='is_active',
        ),
        migrations.AddField(
            model_name='products',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
