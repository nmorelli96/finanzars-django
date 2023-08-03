from collections import defaultdict
from .models import Operacion
from instrumento.models import Especie


def get_unique_activos(user):
    operaciones = Operacion.objects.filter(user=user)
    activos_list = []

    for operacion in operaciones:
        activo = operacion.activo
        if activo not in activos_list:
            activos_list.append(activo)

    return activos_list


def get_operaciones_resumen(user):
    operaciones = Operacion.objects.filter(user=user)
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


def get_operaciones_tenencia(user):
    activos = get_operaciones_resumen(user)
    activos_en_tenencia = []
    for activo in activos:
        if activo["cantidad"] > 0:
            activos_en_tenencia.append(activo)

    for activo in activos_en_tenencia:
        if activo["ticker_mep"] != "":
            if activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS":
                cotiz_especie_mep = (
                    Especie.objects.filter(especie=activo["ticker_mep"], plazo="48hs")[
                        0
                    ].ultimo
                    / 100
                )
                cotiz_especie_ars = (
                    Especie.objects.filter(especie=activo["ticker_ars"], plazo="48hs")[
                        0
                    ].ultimo
                    / 100
                )
                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd

            else:
                cotiz_especie_mep = Especie.objects.filter(
                    especie=activo["ticker_mep"], plazo="48hs"
                )[0].ultimo
                cotiz_especie_ars = Especie.objects.filter(
                    especie=activo["ticker_ars"], plazo="48hs"
                )[0].ultimo
                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd

        else:
            if activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS":
                cotiz_especie_mep = Especie.objects.filter(
                    especie=activo["ticker_ars"], plazo="48hs"
                )[0].ultimo / 100 / (
                    Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo
                    / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
                )
                cotiz_especie_ars = Especie.objects.filter(
                    especie=activo["ticker_ars"], plazo="48hs"
                )[0].ultimo / 100
                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd
            else:
                cotiz_especie_mep = Especie.objects.filter(
                    especie=activo["ticker_ars"], plazo="48hs"
                )[0].ultimo / (
                    Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo
                    / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
                )
                cotiz_especie_ars = Especie.objects.filter(
                    especie=activo["ticker_ars"], plazo="48hs"
                )[0].ultimo
                tenencia_ars = cotiz_especie_ars * activo["cantidad"]
                tenencia_usd = cotiz_especie_mep * activo["cantidad"]
                activo["tenencia_ars"] = tenencia_ars
                activo["tenencia_usd"] = tenencia_usd
    return activos_en_tenencia


def get_operaciones_resultado(user):
    activos = get_operaciones_resumen(user)
    for activo in activos:
        if activo["cantidad"] == 0:
            resultado_ars = -activo["total_ars"]
            resultado_usd = -activo["total_usd"]
            activo["resultado_ars"] = resultado_ars
            activo["resultado_usd"] = resultado_usd
        else:
            if activo["ticker_mep"] != "":
                if activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS":
                    cotiz_especie_mep = (
                        Especie.objects.filter(
                            especie=activo["ticker_mep"], plazo="48hs"
                        )[0].ultimo
                        / 100
                    )
                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo[
                        "total_usd"
                    ]
                    activo["resultado_usd"] = resultado_usd

                    cotiz_especie_ars = (
                        Especie.objects.filter(
                            especie=activo["ticker_ars"], plazo="48hs"
                        )[0].ultimo
                        / 100
                    )
                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo[
                        "total_ars"
                    ]
                    activo["resultado_ars"] = resultado_ars

                else:
                    cotiz_especie_mep = Especie.objects.filter(
                        especie=activo["ticker_mep"], plazo="48hs"
                    )[0].ultimo
                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo[
                        "total_usd"
                    ]
                    activo["resultado_usd"] = resultado_usd

                    cotiz_especie_ars = Especie.objects.filter(
                        especie=activo["ticker_ars"], plazo="48hs"
                    )[0].ultimo
                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo[
                        "total_ars"
                    ]
                    activo["resultado_ars"] = resultado_ars

            else:
                if activo["tipo"] == "ONS" or activo["tipo"] == "BONOS" or activo["tipo"] == "LETRAS":
                    cotiz_especie_mep = Especie.objects.filter(
                        especie=activo["ticker_ars"], plazo="48hs"
                    )[0].ultimo / 100 / (
                        Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo
                        / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
                    )
                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo[
                        "total_usd"
                    ]
                    activo["resultado_usd"] = resultado_usd

                    cotiz_especie_ars = Especie.objects.filter(
                        especie=activo["ticker_ars"], plazo="48hs"
                    )[0].ultimo / 100
                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo[
                        "total_ars"
                    ]
                    activo["resultado_ars"] = resultado_ars
                else:
                    cotiz_especie_mep = Especie.objects.filter(
                    especie=activo["ticker_ars"], plazo="48hs"
                    )[0].ultimo / (
                        Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo
                        / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
                    )
                    resultado_usd = (cotiz_especie_mep * activo["cantidad"]) - activo[
                        "total_usd"
                    ]
                    activo["resultado_usd"] = resultado_usd

                    cotiz_especie_ars = Especie.objects.filter(
                        especie=activo["ticker_ars"], plazo="48hs"
                    )[0].ultimo
                    resultado_ars = (cotiz_especie_ars * activo["cantidad"]) - activo[
                        "total_ars"
                    ]
                    activo["resultado_ars"] = resultado_ars

    return activos
