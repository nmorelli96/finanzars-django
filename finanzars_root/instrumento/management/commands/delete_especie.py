from django.core.management.base import BaseCommand
from instrumento.models import Especie

class Command(BaseCommand):
    help = 'Deletes a row from the Especie model.'

    def add_arguments(self, parser):
        parser.add_argument('especie', type=str, help='especie of the Especie to be deleted')

    def handle(self, *args, **options):
        especie = options['especie']
        try:
            especie = Especie.objects.get(especie=especie)
            especie.delete()
            self.stdout.write(self.style.SUCCESS(f'Especie with especie {especie} deleted successfully.'))
        except Especie.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Especie with especie {especie} does not exist.'))
