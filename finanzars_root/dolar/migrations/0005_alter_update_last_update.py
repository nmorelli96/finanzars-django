# Generated by Django 4.2.4 on 2023-08-20 22:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dolar', '0004_alter_update_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 20, 19, 47, 17, 193686)),
        ),
    ]
