# Generated by Django 4.2.2 on 2023-08-01 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0005_alter_operacion_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacion',
            name='total_ars',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='operacion',
            name='total_usd',
            field=models.FloatField(default=0.0),
        ),
    ]
