# Generated by Django 4.2.4 on 2023-08-27 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instrumento', '0021_especie_usa_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especie_usa',
            name='activo',
        ),
    ]