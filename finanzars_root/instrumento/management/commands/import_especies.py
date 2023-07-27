import csv
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from instrumento.models import Especie, Tipo, Activo
from django.db.models import Q as model_Q

class Command(BaseCommand):
    help = 'Import especies from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        added_count = 0

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                especie=row['especie']
                tipo_value=row['tipo']
                moneda=row['moneda']
                plazo=row['plazo']
                apertura=float(row['apertura'])
                ultimo=float(row['ultimo'])
                cierre_ant=float(row['cierre_ant'])
                var=float(row['var'])
                hora=row['hora']
                punta_compra=row['compra']
                punta_venta=row['venta']
                maximo=row['max']
                minimo=row['min']
                volumen=row['volumen']
                monto=row['monto']

                tipo_instance, created = Tipo.objects.get_or_create(tipo=tipo_value)

                # Search for the Activo based on especie_name in the ticker fields
                activo = Activo.objects.filter(
                    model_Q(ticker_ars=especie) |
                    model_Q(ticker_mep=especie) |
                    model_Q(ticker_ccl=especie)
                ).first()

                try:
                    especie = Especie.objects.create(
                        especie=especie,
                        activo=activo,
                        tipo=tipo_instance,
                        moneda=moneda,
                        plazo=plazo,
                        apertura=apertura,
                        ultimo=ultimo,
                        cierre_ant=cierre_ant,
                        var=var,
                        hora=hora,
                        punta_compra=punta_compra,
                        punta_venta=punta_venta,
                        maximo=maximo,
                        minimo=minimo,
                        volumen=volumen,
                        monto=monto,
                    )
                    added_count += 1
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f'Error importing especie: {especie}. {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'{added_count} especies imported successfully.'))

#python manage.py import_especies instrumento/resources/cedears.csv