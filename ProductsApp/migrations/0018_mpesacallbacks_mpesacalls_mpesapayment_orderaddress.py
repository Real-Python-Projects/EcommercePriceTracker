# Generated by Django 3.1.7 on 2021-04-28 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProductsApp', '0017_auto_20210426_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaCallBacks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_when', models.DateTimeField(auto_now=True)),
                ('ip_address', models.CharField(max_length=200)),
                ('caller', models.CharField(max_length=100)),
                ('conversation_id', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Mpesa Call Back',
                'verbose_name_plural': 'Mpesa Call Backs',
            },
        ),
        migrations.CreateModel(
            name='MpesaCalls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_when', models.DateTimeField(auto_now=True)),
                ('ip_address', models.CharField(max_length=200)),
                ('caller', models.CharField(max_length=100)),
                ('conversation_id', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Mpesa Call',
                'verbose_name_plural': 'Mpesa Calls',
            },
        ),
        migrations.CreateModel(
            name='MpesaPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_when', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('organization_balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Mpesa Payment',
                'verbose_name_plural': 'Mpesa Payments',
            },
        ),
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('street_address2', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('post_address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]