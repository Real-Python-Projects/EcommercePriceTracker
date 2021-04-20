# Generated by Django 3.1.7 on 2021-04-20 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_phonenumber_date_added'),
        ('ProductsApp', '0009_auto_20210420_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='merchant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='User.merchantuser'),
            preserve_default=False,
        ),
    ]
