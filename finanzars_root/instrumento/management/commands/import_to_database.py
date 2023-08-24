from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from instrumento.models import Especie, Tipo, Activo, Especie_USA
from django.db.models import Q

def import_to_database(df):
    added_count = 0

    for _, row in df.iterrows():
        especie = row.name
        plazo = row["plazo"]

        tipo_value = row["tipo"]
        moneda = row["moneda"]
        apertura = row["apertura"]
        ultimo = row["ultimo"]
        cierre_ant = row["cierre_ant"]
        var = row["var"]
        hora = row["hora"]
        punta_compra = row["compra"]
        punta_venta = row["venta"]
        maximo = row["max"]
        minimo = row["min"]
        volumen = row["volumen"]
        monto = row["monto"]

        # Buscar o crear el Tipo de la Especie
        tipo_instance, created = Tipo.objects.get_or_create(tipo=tipo_value)

        # Buscar o crear el Activo basado en el nombre de la especie en los campos de ticker
        activo = Activo.objects.filter(
            Q(ticker_ars=especie) |
            Q(ticker_mep=especie) |
            Q(ticker_ccl=especie)
        ).first()

        try:
            especie_obj, created = Especie.objects.update_or_create(
                especie=especie,
                plazo=plazo,
                defaults={
                    "activo": activo,
                    "tipo": tipo_instance,
                    "moneda": moneda,
                    "apertura": apertura,
                    "ultimo": ultimo,
                    "cierre_ant": cierre_ant,
                    "var": var,
                    "hora": hora,
                    "punta_compra": punta_compra,
                    "punta_venta": punta_venta,
                    "maximo": maximo,
                    "minimo": minimo,
                    "volumen": volumen,
                    "monto": monto,
                }
            )
            added_count += 1
        except IntegrityError as e:
            print(f'Error importing especie: {especie}. {str(e)}')

    print(f"{added_count} especies imported successfully.")

def import_to_database_usa(df):
    added_count = 0

    for _, row in df.iterrows():
        especie = row.name  # Utiliza el índice de fila como especie

        nombre = row['nombre']
        ultimo = float(row['ultimo'])
        var = float(row['var'])
        hora = row['hora']

        try:
            especie_usa_obj, created = Especie_USA.objects.update_or_create(
                # usa el campo especie como criterio de busqueda y 
                # los otros campos se pasan como argumentos en el diccionario defaults
                especie=especie,
                defaults={
                    'nombre': nombre,
                    'ultimo': ultimo,
                    'var': var,
                    'hora': hora,
                }
            )
            added_count += 1
        except IntegrityError as e:
            print(f'Error importing especie_usa: {especie}. {str(e)}')

    print(f"{added_count} especies_usa imported successfully.")
