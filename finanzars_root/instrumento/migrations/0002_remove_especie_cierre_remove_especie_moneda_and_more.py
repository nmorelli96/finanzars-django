# Generated by Django 4.2.2 on 2023-06-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especie',
            name='cierre',
        ),
        migrations.RemoveField(
            model_name='especie',
            name='moneda',
        ),
        migrations.AlterField(
            model_name='especie',
            name='hora',
            field=models.CharField(max_length=8),
        ),
    ]
