from django.db.utils import IntegrityError
from instrumento.models import Especie, Tipo, Activo, Especie_USA
from django.db.models import Q
from datetime import datetime, timedelta
import pandas as pd
import gc


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
        hora_scrapped = row["hora"]
        punta_compra = row["compra"]
        punta_venta = row["venta"]
        maximo = row["max"]
        minimo = row["min"]
        volumen = row["volumen"]
        monto = row["monto"]

        actualizado = datetime.now()

        tipo_instance, created = Tipo.objects.get_or_create(tipo=tipo_value)

        # Buscar o crear el Activo basado en el nombre de la especie en los campos de ticker
        activo = Activo.objects.filter(
            Q(ticker_ars=especie) |
            Q(ticker_mep=especie) |
            Q(ticker_ccl=especie)
        ).first()

        if pd.isna(hora_scrapped):
            fecha_hora_str = hora_scrapped
        else:
            hora_scrapped = str(hora_scrapped)
            fecha_actual = datetime.now().date()
            hora_obj = datetime.strptime(hora_scrapped, '%H:%M:%S').time()
            fecha_hora_completa = datetime.combine(fecha_actual, hora_obj)
            fecha_hora_str = fecha_hora_completa.strftime('%Y-%m-%d %H:%M:%S')

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
                    "hora": fecha_hora_str,
                    "punta_compra": punta_compra,
                    "punta_venta": punta_venta,
                    "maximo": maximo,
                    "minimo": minimo,
                    "volumen": volumen,
                    "monto": monto,
                    "actualizado" : actualizado,
                }
            )
            added_count += 1
        except IntegrityError as e:
            print(f'Error importing especie: {especie}. {str(e)}')

    del df
    gc.collect()
    print(f"{added_count} especies imported successfully.")

def import_to_database_usa(json):
    added_count = 0
    data = json

    rows = data["data"]["rows"]

    for row in rows:
        especie = row["symbol"]
        nombre = row["name"][:40]
        ultimo = float(row["lastsale"].replace('$', '').replace(',', ''))
        var_str = row["pctchange"].replace('%', '').replace(',', '')
        var = round(float(var_str), 2)
        hora = datetime.now()

        actualizado = datetime.now()

        try:
            especie_usa_obj, created = Especie_USA.objects.update_or_create(
                especie=especie,
                defaults={
                    'nombre': nombre,
                    'ultimo': ultimo,
                    'var': var,
                    'hora': hora,
                    'actualizado': actualizado,
                }
            )
            added_count += 1
        except IntegrityError as e:
            print(f'Error importing especie_usa: {especie}. {str(e)}')
    
    del data
    gc.collect()
    print(f"{added_count} especies_usa imported successfully.")
