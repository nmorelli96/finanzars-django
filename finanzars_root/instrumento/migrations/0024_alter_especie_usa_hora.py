# Generated by Django 4.2.4 on 2023-08-29 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumento', '0023_alter_especie_monto_alter_especie_volumen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especie_usa',
            name='hora',
            field=models.CharField(max_length=30),
        ),
    ]
