# Generated by Django 3.1.7 on 2021-04-21 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20210421_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonenumber',
            old_name='is_activated',
            new_name='is_verified',
        ),
    ]
