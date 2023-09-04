from django.utils import timezone
import gc

from .import_to_database import import_to_database, import_to_database_usa
from .clean_scrap_data import clean_scrap_data
from .scrap_bonos import scrap_bonos
from .scrap_cedears import scrap_cedears
from .scrap_letras import scrap_letras
from .scrap_merval import scrap_merval
from .scrap_ons import scrap_ons
from .scrap_usa import scrap_usa
from dolar.utils import fetch_fiat, fetch_bancos, fetch_binance, fetch_cryptos

import warnings
from django.core.management.base import BaseCommand

warnings.filterwarnings("ignore", "DateTimeField .* received a naive datetime .* while time zone support is active.", RuntimeWarning)


class Command(BaseCommand):

  def handle(self, *args, **options):

  # def update_especies():
    bonos_df = clean_scrap_data(scrap_bonos())
    cedears_df = clean_scrap_data(scrap_cedears())
    letras_df = clean_scrap_data(scrap_letras())
    merval_df = clean_scrap_data(scrap_merval())
    ons_df = clean_scrap_data(scrap_ons())
    usa_df = scrap_usa()

    import_to_database(bonos_df)
    import_to_database(cedears_df)
    import_to_database(letras_df)
    import_to_database(merval_df)
    import_to_database(ons_df)
    import_to_database_usa(usa_df)

def actualizar_bursatiles():
  bonos_df = clean_scrap_data(scrap_bonos())
  cedears_df = clean_scrap_data(scrap_cedears())
  letras_df = clean_scrap_data(scrap_letras())
  merval_df = clean_scrap_data(scrap_merval())
  ons_df = clean_scrap_data(scrap_ons())
  usa_df = scrap_usa()
  import_to_database(bonos_df)
  import_to_database(cedears_df)
  import_to_database(letras_df)
  import_to_database(merval_df)
  import_to_database(ons_df)
  import_to_database_usa(usa_df)
  del bonos_df, cedears_df, letras_df, merval_df, ons_df, usa_df
  gc.collect()
  ahora = timezone.now()
  print(f"actualizar_bursatiles ejecutada en: {ahora}")


def actualizar_bonos():
  bonos_df = clean_scrap_data(scrap_bonos())
  import_to_database(bonos_df)
  ahora = timezone.now()
  del bonos_df
  gc.collect()
  print(f"actualizar_bonos ejecutada en: {ahora}")

def actualizar_cedears():
  cedears_df = clean_scrap_data(scrap_cedears())
  import_to_database(cedears_df)
  ahora = timezone.now()
  del cedears_df
  gc.collect()
  print(f"actualizar_cedears ejecutada en: {ahora}")

def actualizar_letras():
  letras_df = clean_scrap_data(scrap_letras())
  import_to_database(letras_df)
  ahora = timezone.now()
  del letras_df
  gc.collect()
  print(f"actualizar_letras ejecutada en: {ahora}")

def actualizar_merval():
  merval_df = clean_scrap_data(scrap_merval())
  import_to_database(merval_df)
  ahora = timezone.now()
  del merval_df
  gc.collect()
  print(f"actualizar_merval ejecutada en: {ahora}")

def actualizar_ons():
  ons_df = clean_scrap_data(scrap_ons())
  import_to_database(ons_df)
  ahora = timezone.now()
  del ons_df
  gc.collect()
  print(f"actualizar_ons ejecutada en: {ahora}")

def actualizar_usa():
  usa_df = scrap_usa()
  import_to_database_usa(usa_df)
  ahora = timezone.now()
  del usa_df
  gc.collect()
  print(f"actualizar_usa ejecutada en: {ahora}")


def actualizar_dolar():
  fetch_fiat()
  fetch_bancos()
  fetch_binance()
  fetch_cryptos()
  ahora = timezone.now()
  print(f"actualizar_dolar ejecutada en: {ahora}")


