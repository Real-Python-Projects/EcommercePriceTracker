# Generated by Django 3.1.7 on 2021-04-30 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0018_mpesacallbacks_mpesacalls_mpesapayment_orderaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('slug', models.SlugField(blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='producttags',
            name='title',
        ),
        migrations.AddField(
            model_name='producttags',
            name='tags',
            field=models.ManyToManyField(to='ProductsApp.Tags'),
        ),
    ]