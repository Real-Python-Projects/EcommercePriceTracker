# Generated by Django 3.1.7 on 2021-04-20 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_phonenumber_profile'),
        ('ProductsApp', '0007_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProductsApp.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customeruser')),
            ],
            options={
                'verbose_name': 'Wishlist item',
                'verbose_name_plural': 'wishlist items',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CustomerWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(to='ProductsApp.WishListItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.customeruser')),
            ],
            options={
                'verbose_name': 'Customer Wishlist item',
                'verbose_name_plural': 'Customer wishlist items',
                'ordering': ['-timestamp'],
            },
        ),
    ]
