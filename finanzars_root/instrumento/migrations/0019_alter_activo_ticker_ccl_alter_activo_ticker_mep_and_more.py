# Generated by Django 4.2.2 on 2023-08-02 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumento', '0018_alter_activo_ticker_ccl_alter_activo_ticker_mep_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activo',
            name='ticker_ccl',
            field=models.CharField(blank=True, default='', help_text='5 caracteres máx.', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activo',
            name='ticker_mep',
            field=models.CharField(blank=True, default='', help_text='5 caracteres máx.', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activo',
            name='ticker_usa',
            field=models.CharField(blank=True, default='', help_text='5 caracteres máx.', max_length=5),
            preserve_default=False,
        ),
    ]
