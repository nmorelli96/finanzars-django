# Generated by Django 4.2.4 on 2023-08-19 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dolar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='binance',
            name='coin',
        ),
        migrations.RemoveField(
            model_name='binance',
            name='operation',
        ),
    ]
