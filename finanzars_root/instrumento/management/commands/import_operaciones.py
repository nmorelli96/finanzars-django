import csv
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from instrumento.models import Especie, Tipo, Activo
from cartera.models import Operacion

class Command(BaseCommand):
    help = 'Import operaciones from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        added_count = 0
        user = User.objects.first()

        with open(csv_file, 'r', encoding='latin1') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                user = user
                tipo_value=row['tipo']
                plazo=row['plazo']
                activo_value=row['activo']
                especie_value=row['especie']
                fecha=row['fecha']
                cotiz_mep=float(row['cotiz_mep'].replace('.', '').replace(',', '.'))
                operacion=row['operacion']
                cantidad=int(row['cantidad'].replace('.', ''))
                precio_ars=float(row['precio_ars'].replace('.', '').replace(',', '.'))
                precio_usd=float(row['precio_usd'].replace('.', '').replace(',', '.'))
                total_ars=float(row['total_ars'].replace('.', '').replace(',', '.'))
                total_usd=float(row['total_usd'].replace('.', '').replace(',', '.'))

                tipo_instance, created = Tipo.objects.get_or_create(tipo=tipo_value)
                activo_instance, created = Activo.objects.get_or_create(ticker_ars=activo_value)
                especie_instance, created = Especie.objects.get_or_create(especie=especie_value, plazo=plazo)

                operacion = Operacion.objects.create(
                    user = user,
                    tipo = tipo_instance,
                    plazo = plazo,
                    activo = activo_instance,
                    especie = especie_instance,
                    fecha = fecha,
                    cotiz_mep = cotiz_mep,
                    operacion = operacion,
                    cantidad = cantidad,
                    precio_ars = precio_ars,
                    precio_usd = precio_usd,
                    total_ars = total_ars,
                    total_usd = total_usd,
                )
                added_count += 1

        self.stdout.write(self.style.SUCCESS(f'{added_count} operaciones imported successfully.'))

#python manage.py import_especies instrumento/resources/cedears.csv