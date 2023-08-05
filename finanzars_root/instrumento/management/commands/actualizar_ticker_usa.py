import csv
from django.core.management.base import BaseCommand
from instrumento.models import Activo, Tipo

class Command(BaseCommand):
    help = 'Actualiza el campo ticker_usa de los activos cedears desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Ruta al archivo CSV con los tickers USA')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        self.actualizar_ticker_usa(csv_file)

    def actualizar_ticker_usa(self, csv_file):
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

                try:
                    activo = Activo.objects.get(ticker_ars=ticker_ars)
                    activo.ticker_usa = ticker_usa
                    activo.save()
                    self.stdout.write(self.style.SUCCESS(f"Actualizado ticker_usa para {ticker_ars} a {ticker_usa}"))
                except Activo.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f"No se encontró el activo con ticker_ars {ticker_ars}"))
