# Generated by Django 4.2.2 on 2023-07-05 00:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0003_remove_operacion_moneda_operacion_activo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacion',
            name='plazo',
            field=models.CharField(choices=[('CI', 'CI'), ('24hs', '24hs'), ('48hs', '48hs')], default='48hs', max_length=4),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 4, 21, 5, 5, 98398)),
        ),
    ]
