import csv
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from instrumento.models import Especie_USA

class Command(BaseCommand):
    help = 'Import Especies_USA from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        added_count = 0

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                especie=row['especie']
                nombre=row['nombre']
                ultimo=float(row['ultimo'])
                var=float(row['var'])
                hora=row['hora']

                try:
                    especie = Especie_USA.objects.create(
                        especie=especie,
						nombre=nombre,
                        ultimo=ultimo,
                        var=var,
                        hora=hora,
                    )
                    added_count += 1
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f'Error importing especie: {especie}. {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'{added_count} Especies_USA imported successfully.'))
