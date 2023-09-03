from collections import defaultdict
from .models import Operacion
from instrumento.models import Especie
from collections import defaultdict


def get_unique_activos(user):
    operaciones = Operacion.objects.filter(user=user)
    activos_list = []

    for operacion in operaciones:
        activo = operacion.activo
        if activo not in activos_list:
            activos_list.append(activo)

    return activos_list


def get_operaciones_resumen(user, id_operacion_a_editar=None):
    operaciones = Operacion.objects.filter(user=user)

    if id_operacion_a_editar:
        operaciones = operaciones.exclude(id=id_operacion_a_editar)

    activos_dict = defaultdict(
        lambda: {
            "activo": None,
            "tipo": None,
            "ticker_ars": None,
            "ticker_mep": None,
            "cantidad": 0,
            "total_ars": 0,
            "total_usd": 0,
        }
    )

    for operacion in operaciones:
        activo = operacion.activo
        tipo = activo.tipo.tipo
        ticker_ars = activo.ticker_ars
        ticker_mep = activo.ticker_mep
        cantidad = operacion.cantidad
        precio_ars = operacion.precio_ars
        precio_usd = operacion.precio_usd
        total_ars = operacion.total_ars
        total_usd = operacion.total_usd

        activos_dict[activo]["activo"] = activo
        activos_dict[activo]["tipo"] = tipo
        activos_dict[activo]["ticker_ars"] = ticker_ars
        activos_dict[activo]["ticker_mep"] = ticker_mep
        activos_dict[activo]["cantidad"] += cantidad
        if (operacion.operacion == "Venta") | (operacion.operacion == "Compra"):
            activos_dict[activo]["total_ars"] += cantidad * precio_ars
            activos_dict[activo]["total_usd"] += cantidad * precio_usd
        else:
            activos_dict[activo]["total_ars"] += total_ars
            activos_dict[activo]["total_usd"] += total_usd

    activos_list = list(activos_dict.values())
    return activos_list


def get_operaciones_tenencia(user, in_operacion_a_editar=None):
    activos = get_operaciones_resumen(user, in_operacion_a_editar)
    mep = (
        Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo
        / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    )
    activos_en_tenencia = []
    for activo in activos:
        if activo["cantidad"] > 0:
            activos_en_tenencia.append(activo)

    for activo in activos_en_tenencia:
        cotiz_ars = Especie.objects.filter(especie=activo["ticker_ars"], plazo="48hs")[0]

        # Si tiene contrapartida D
        if activo["ticker_mep"] != "":
            cotiz_mep = Especie.objects.filter(especie=activo["ticker_mep"], plazo="48hs")[0]

            # Si es Bono, ON o Letra
            if (activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS"):

                cotiz_especie_mep = (cotiz_mep.ultimo / 100)
                cotiz_especie_ars = (cotiz_ars.ultimo / 100)

                # Si no hay precio "ultimo"
                if cotiz_especie_mep == 0:
                    cotiz_especie_mep = (cotiz_mep.punta_venta / 100)
                if cotiz_especie_ars == 0:
                    cotiz_especie_ars = (cotiz_ars.punta_venta / 100)

                print(cotiz_especie_ars, cotiz_especie_mep)
                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd

            # Si es CEDEAR o MERVAL
            else:
                cotiz_especie_mep = cotiz_mep.ultimo
                cotiz_especie_ars = cotiz_ars.ultimo

                # Si no hay precio "ultimo"
                if cotiz_especie_mep == 0:
                    cotiz_especie_mep = cotiz_mep.punta_venta
                if cotiz_especie_ars == 0:
                    cotiz_especie_ars = cotiz_ars.punta_venta

                print(cotiz_especie_ars, cotiz_especie_mep)
                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd

        # Si NO tiene contrapartida D
        else:
            # Si es Bono, ON o Letra
            if (activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS"):

                cotiz_especie_mep = (cotiz_ars.ultimo / 100 / mep)
                cotiz_especie_ars = (cotiz_ars.ultimo / 100)

                # Si no hay precio "ultimo"
                if cotiz_especie_mep == 0:
                    cotiz_especie_mep = (cotiz_ars.punta_venta / 100 / mep )
                if cotiz_especie_ars == 0:
                    cotiz_especie_ars = (cotiz_ars.punta_venta / 100)

                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd

            # Si es CEDEAR o MERVAL
            else:
                cotiz_especie_mep = cotiz_ars.ultimo / mep
                cotiz_especie_ars = cotiz_ars.ultimo

                # Si no hay precio "ultimo"
                if cotiz_especie_mep == 0:
                    cotiz_especie_mep = cotiz_ars.punta_venta / mep
                if cotiz_especie_ars == 0:
                    cotiz_especie_ars = cotiz_ars.punta_venta

                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd
    return activos_en_tenencia


def get_operaciones_resultado(user):
    activos = get_operaciones_resumen(user)
    mep = (
        Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo
        / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    )

    for activo in activos:
        if activo["cantidad"] == 0:
            resultado_ars = -activo["total_ars"]
            resultado_usd = -activo["total_usd"]
            activo["resultado_ars"] = resultado_ars
            activo["resultado_usd"] = resultado_usd

        else:
            cotiz_ars = Especie.objects.filter(especie=activo["ticker_ars"], plazo="48hs")[0]
            # Si tiene contrapartida D
            if activo["ticker_mep"] != "":
                cotiz_mep = Especie.objects.filter(especie=activo["ticker_mep"], plazo="48hs")[0]

                # Si es Bono, ON o Letra
                if (activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS"):

                    cotiz_especie_mep = (cotiz_mep.ultimo / 100)

                    if cotiz_especie_mep == 0:
                        cotiz_especie_mep = (cotiz_mep.punta_venta / 100)

                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo["total_usd"]
                    activo["resultado_usd"] = resultado_usd

                    cotiz_especie_ars = (cotiz_ars.ultimo / 100)

                    if cotiz_especie_ars == 0:
                        cotiz_especie_ars = (cotiz_ars.punta_venta / 100)

                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo["total_ars"]
                    activo["resultado_ars"] = resultado_ars

                # Si es CEDEAR o MERVAL
                else:
                    cotiz_especie_mep = cotiz_mep.ultimo

                    if cotiz_especie_mep == 0:
                        cotiz_especie_mep = cotiz_mep.punta_venta

                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo["total_usd"]
                    activo["resultado_usd"] = resultado_usd

                    cotiz_especie_ars = cotiz_ars.ultimo

                    if cotiz_especie_ars == 0:
                        cotiz_especie_ars = cotiz_ars.punta_venta

                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo["total_ars"]
                    activo["resultado_ars"] = resultado_ars

            # Si NO tiene contrapartida D
            else:

                # Si es Bono, ON o Letra
                if (activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS"):

                    if cotiz_ars.ultimo == 0:
                        cotiz_especie_ars = cotiz_ars.punta_venta / 100
                    else:
                        cotiz_especie_ars = cotiz_ars.ultimo / 100

                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo["total_ars"]

                    if cotiz_ars.ultimo == 0:
                        cotiz_especie_mep = cotiz_ars.punta_venta / 100 / mep
                    else:
                        cotiz_especie_mep = cotiz_ars.ultimo / 100 / mep

                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo["total_usd"]

                    activo["resultado_ars"] = resultado_ars
                    activo["resultado_usd"] = resultado_usd

                # Si es CEDEAR o MERVAL
                else:
                    if cotiz_ars.ultimo == 0:
                        cotiz_especie_ars = cotiz_ars.punta_venta
                    else:
                        cotiz_especie_ars = cotiz_ars.ultimo

                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo["total_ars"]

                    if cotiz_ars.ultimo == 0:
                        cotiz_especie_mep = cotiz_ars.punta_venta / mep
                    else:
                        cotiz_especie_mep = cotiz_ars.ultimo / mep

                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo["total_usd"]

                    activo["resultado_ars"] = resultado_ars
                    activo["resultado_usd"] = resultado_usd

    return activos
