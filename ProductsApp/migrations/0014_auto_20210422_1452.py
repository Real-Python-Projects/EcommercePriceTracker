# Generated by Django 3.1.7 on 2021-04-22 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_auto_20210421_1738'),
        ('ProductsApp', '0013_auto_20210421_1001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='shop',
            name='merchant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.merchantuser'),
        ),
    ]