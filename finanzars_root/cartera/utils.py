from collections import defaultdict
from .models import Operacion
from instrumento.models import Especie
from collections import defaultdict

def get_unique_activos(user):
    operaciones = Operacion.objects.filter(user=user)
    activos_set = set(operacion.activo for operacion in operaciones)
    return list(activos_set)

def calculate_tenencia(activo, cotiz_ars, cotiz_mep, cantidad, tipo, mep):
    if tipo in ["ONS", "BONOS", "LETRAS"]:
        if cotiz_mep != None:
            if cotiz_mep.ultimo != 0:
                cotiz_especie_mep = cotiz_mep.ultimo / 100
            else:
                cotiz_especie_mep = cotiz_mep.punta_venta / 100

            if cotiz_ars.ultimo != 0:
                cotiz_especie_ars = cotiz_ars.ultimo / 100
            else:
                cotiz_especie_ars = cotiz_ars.punta_venta / 100
        else:
            if cotiz_ars.ultimo != 0:
                cotiz_especie_mep = cotiz_ars.ultimo / 100 / mep
                cotiz_especie_ars = cotiz_ars.ultimo / 100
            else:
                cotiz_especie_mep = cotiz_ars.punta_venta / 100 / mep
                cotiz_especie_ars = cotiz_ars.punta_venta / 100
    else:
        if cotiz_mep != None:
            if cotiz_mep.ultimo != 0:
                cotiz_especie_mep = cotiz_mep.ultimo
            else:
                cotiz_especie_mep = cotiz_mep.punta_venta 
            if cotiz_ars.ultimo != 0:
                cotiz_especie_ars = cotiz_ars.ultimo
            else:
                cotiz_especie_ars = cotiz_ars.punta_venta
        else:
            if cotiz_ars.ultimo != 0:
                cotiz_especie_mep = cotiz_ars.ultimo / mep
                cotiz_especie_ars = cotiz_ars.ultimo
            else:
                cotiz_especie_mep = cotiz_ars.punta_venta / mep
                cotiz_especie_ars = cotiz_ars.punta_venta

    tenencia_ars = cotiz_especie_ars * cantidad
    tenencia_usd = cotiz_especie_mep * cantidad

    return tenencia_ars, tenencia_usd

def calculate_resultado(activo, cotiz_ars, cotiz_mep, cantidad, tipo, mep):
    #if cotiz_mep != None:
    #    print(activo, "cotiz_ars:", cotiz_ars.ultimo, cotiz_ars.punta_venta, "cotiz_mep:", cotiz_mep.ultimo, cotiz_mep.punta_venta, "cantidad:", cantidad, "tipo:", tipo, mep)
    #else:
    #    print(activo, "cotiz_ars:", cotiz_ars.ultimo, cotiz_ars.punta_venta, "cotiz_mep:", cotiz_mep, "cantidad:", cantidad, "tipo:", tipo, mep)
    if cantidad == 0:
        resultado_ars = -activo["total_ars"]
        resultado_usd = -activo["total_usd"]
    else:
        if tipo in ["ONS", "BONOS", "LETRAS"]:
            if cotiz_mep != None:
                if cotiz_mep.ultimo != 0:
                    cotiz_especie_mep = cotiz_mep.ultimo / 100
                else:
                    cotiz_especie_mep = cotiz_mep.punta_venta / 100
                if cotiz_ars.ultimo != 0:
                    cotiz_especie_ars = cotiz_ars.ultimo / 100
                else:
                    cotiz_especie_ars = cotiz_ars.punta_venta / 100
            else:
                if cotiz_ars.ultimo != 0:
                    cotiz_especie_mep = cotiz_ars.ultimo / 100 / mep
                    cotiz_especie_ars = cotiz_ars.ultimo / 100
                else:
                    cotiz_especie_mep = cotiz_ars.punta_venta / 100 / mep
                    cotiz_especie_ars = cotiz_ars.punta_venta / 100
        else:
            if cotiz_mep != None:
                if cotiz_mep.ultimo != 0:
                    cotiz_especie_mep = cotiz_mep.ultimo
                else:
                    cotiz_especie_mep = cotiz_mep.punta_venta 
                if cotiz_ars.ultimo != 0:
                    cotiz_especie_ars = cotiz_ars.ultimo
                else:
                    cotiz_especie_ars = cotiz_ars.punta_venta
            else:
                if cotiz_ars.ultimo != 0:
                    cotiz_especie_mep = cotiz_ars.ultimo / mep
                    cotiz_especie_ars = cotiz_ars.ultimo
                else:
                    cotiz_especie_mep = cotiz_ars.punta_venta / mep
                    cotiz_especie_ars = cotiz_ars.punta_venta

        resultado_usd = (cotiz_especie_mep * cantidad) - activo["total_usd"]
        resultado_ars = (cotiz_especie_ars * cantidad) - activo["total_ars"]

    return resultado_ars, resultado_usd

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

        if operacion.operacion in ["Venta", "Compra"]:
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

    activos_en_tenencia = [activo for activo in activos if activo["cantidad"] > 0]

    for activo in activos_en_tenencia:
        cotiz_ars = Especie.objects.filter(especie=activo["ticker_ars"], plazo="48hs")[0]
        cotiz_mep = None

        if activo["ticker_mep"]:
            cotiz_mep = Especie.objects.filter(especie=activo["ticker_mep"], plazo="48hs")[0]

        tenencia_ars, tenencia_usd = calculate_tenencia(activo, cotiz_ars, cotiz_mep, activo["cantidad"], activo["tipo"], mep)

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
        cotiz_ars = Especie.objects.filter(especie=activo["ticker_ars"], plazo="48hs")[0]
        cotiz_mep = None
        
        if activo["ticker_mep"]:
            cotiz_mep = Especie.objects.filter(especie=activo["ticker_mep"], plazo="48hs")[0]

        resultado_ars, resultado_usd = calculate_resultado(activo, cotiz_ars, cotiz_mep, activo["cantidad"], activo["tipo"], mep)

        activo["resultado_ars"] = resultado_ars
        activo["resultado_usd"] = resultado_usd

    return activos
