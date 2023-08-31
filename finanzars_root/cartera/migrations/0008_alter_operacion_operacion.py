# Generated by Django 4.2.4 on 2023-08-31 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartera', '0007_operacion_actualizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacion',
            name='operacion',
            field=models.CharField(choices=[('Compra', 'Compra'), ('Venta', 'Venta'), ('Dividendo', 'Dividendo'), ('Renta', 'Renta'), ('Amortización', 'Amortización')], default='Compra', max_length=30),
        ),
    ]