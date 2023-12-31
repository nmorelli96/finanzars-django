# Generated by Django 4.2.2 on 2023-07-04 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instrumento', '0011_remove_especie_nombre_especie_moneda_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activo',
            options={'verbose_name_plural': 'Activos'},
        ),
        migrations.AlterModelOptions(
            name='especie',
            options={'ordering': ('tipo', 'especie'), 'verbose_name_plural': 'Especies'},
        ),
        migrations.AddField(
            model_name='especie',
            name='activo',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='especies', to='instrumento.activo'),
        ),
        migrations.AlterField(
            model_name='especie',
            name='moneda',
            field=models.CharField(choices=[('MEP', 'MEP'), ('CCL', 'CCL'), ('ARS', 'ARS')], default='ARS', max_length=3),
        ),
        migrations.AlterField(
            model_name='especie',
            name='plazo',
            field=models.CharField(choices=[('CI', 'CI'), ('24hs', '24hs'), ('48hs', '48hs')], default='48hs', max_length=4),
        ),
    ]
