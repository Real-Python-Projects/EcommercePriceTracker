# Generated by Django 3.1.7 on 2021-04-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0002_auto_20210416_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
