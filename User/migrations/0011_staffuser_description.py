# Generated by Django 3.1.7 on 2021-05-03 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_auto_20210503_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffuser',
            name='description',
            field=models.TextField(default='No description'),
        ),
    ]