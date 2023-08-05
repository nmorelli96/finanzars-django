import csv
from django.core.management.base import BaseCommand
from instrumento.models import Especie, Tipo, Activo

class Command(BaseCommand):
    help = 'Import activos from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        added_count = 0

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tipo_value=row['tipo']
                ticker_ars=row['ticker_ars']
                ticker_mep=row['ticker_mep']
                ticker_ccl=row['ticker_ccl']
                ticker_usa=row['ticker_usa']
                nombre=row['nombre']
                mercado=row['mercado']
                ratio=float(row['ratio'])

                tipo_instance, created = Tipo.objects.get_or_create(tipo=tipo_value)

                activo = Activo.objects.create(
                    tipo = tipo_instance,
                    ticker_ars = ticker_ars,
                    ticker_mep = ticker_mep,
                    ticker_ccl = ticker_ccl,
                    ticker_usa = ticker_usa,
                    nombre = nombre,
                    mercado = mercado,
                    ratio = ratio
                )
                added_count += 1

        self.stdout.write(self.style.SUCCESS(f'{added_count} activos imported successfully.'))

#python manage.py import_especies instrumento/resources/cedears.csv