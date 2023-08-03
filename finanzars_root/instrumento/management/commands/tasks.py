from .import_to_database import import_to_database
from .clean_scrap_data import clean_scrap_data
from .scrap_bonos import scrap_bonos
from .scrap_cedears import scrap_cedears
from .scrap_letras import scrap_letras
from .scrap_merval import scrap_merval
from .scrap_ons import scrap_ons
from .scrap_usa import scrap_usa
import warnings

warnings.filterwarnings("ignore", "DateTimeField .* received a naive datetime .* while time zone support is active.", RuntimeWarning)

from django.core.management.base import BaseCommand

class Command(BaseCommand):

  def handle(self, *args, **options):

  # def update_especies():
    bonos_df = clean_scrap_data(scrap_bonos())
    cedears_df = clean_scrap_data(scrap_cedears())
    letras_df = clean_scrap_data(scrap_letras())
    merval_df = clean_scrap_data(scrap_merval())
    ons_df = clean_scrap_data(scrap_ons())
    #usa_df = clean_scrap_data(scrap_usa())

    import_to_database(bonos_df)
    import_to_database(cedears_df)
    import_to_database(letras_df)
    import_to_database(merval_df)
    import_to_database(ons_df)
    #import_to_database(usa_df)