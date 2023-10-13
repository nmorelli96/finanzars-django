from django.shortcuts import render, redirect
from collections import namedtuple
from datetime import datetime
from .tables import BancosTable, FiatTable, CryptosTable
import dolar.models as models
from instrumento.models import Especie


def dolar(request):
    
    bancos_data = models.Banco.objects.all().values()
    Banco = namedtuple("Banco", ["banco", "compra", "venta", "ventaTot", "hora"])

    bancos_mapping = {
        "Balanz": "balanz",
        "Hipotecario": "hipotecario",
        "ICBC": "icbc",
        "Supervielle": "supervielle",
        "Brubank": "brubank",
        "Ciudad": "ciudad",
        "Provincia": "bapro",
        "HSBC": "hsbc",
        "Macro": "macro",
        "Patagonia": "patagonia",
        "BBVA": "bbva",
        "Galicia": "galicia",
        "Santander": "santander",
        "Reba": "rebanking",
        "Nación": "bna",
        "CambioAR": "cambioar",
        "Plus": "plus",
    }

    bancos = []
    for banco_data in bancos_data:
        banco_data_dict = banco_data.get("data", {})
        for key, value in banco_data_dict.items():
            if key in ["rebanking", "buendolar", "globalcambio", "naranjax", "dolaria", "dolariol", "cambioposadas", "prex", "cambiodieza", "davsa", "triacambio", "plazacambio", "cambiosroca"]:
                continue
            elif key != "_id":
                banco_nombre = next(
                    (k for k, v in bancos_mapping.items() if v == key), key
                )
                banco = Banco(
                    banco=banco_nombre,
                    compra=value.get("bid"),
                    venta=value.get("totalAsk") / 1.75,
                    ventaTot=value.get("totalAsk"),
                    hora=value.get("time"),
                )
                bancos.append(banco)

    bancos_table = BancosTable(bancos, order_by=request.GET.get("sort"))


    fiat_data = models.Fiat.objects.values("data").first()
    fiat_data_last = models.Fiat.objects.values("data_last").first()
    fiat_data_dict = fiat_data.get("data", {})
    fiat_data_last_dict = fiat_data_last.get("data_last", {})
    print(fiat_data_dict)
    print(fiat_data_last)
    Fiat = namedtuple("Fiat", ["dolar", "venta", "compra", "var"])
    fiatHora = datetime.fromtimestamp(fiat_data_dict["time"]).strftime("%Y-%m-%d %H:%M:%S")
    binance_data = models.Binance.objects.values("data").first()


    try:
        mep = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    except:
        mep = fiat_data_dict["mepgd30"]

    try:
        ccl = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30C", plazo="48hs")[0].ultimo
    except:  
        ccl = fiat_data_dict["cclgd30"]

    fiat = [
        Fiat(dolar="Oficial", venta=fiat_data_dict["oficial"], compra=banco_data_dict["bna"]["totalBid"], 
             var=(fiat_data_dict["oficial"]/fiat_data_last_dict["oficial"] - 1) * 100),
        Fiat(dolar="Solidario", venta=fiat_data_dict["solidario"], compra=banco_data_dict["bna"]["totalBid"], 
             var=(fiat_data_dict["oficial"]/fiat_data_last_dict["oficial"] - 1) * 100),
        Fiat(dolar="Blue", venta=fiat_data_dict["blue"], compra=fiat_data_dict["blue_bid"], 
             var=(fiat_data_dict["blue"]/fiat_data_last_dict["blue"] - 1) * 100),
        Fiat(dolar="Crypto", venta=binance_data["data"][0]["Binance"]["price"], compra=binance_data["data"][1]["Binance"]["price"],
             var=(float(binance_data["data"][0]["Binance"]["price"]) / float(fiat_data_last_dict["crypto"]) - 1) * 100),
        Fiat(dolar="MEP GD30", venta=mep, compra=mep, 
             var=(mep/fiat_data_last_dict["mep_gd30"] - 1) * 100),
        Fiat(dolar="CCL GD30", venta=ccl, compra=ccl, 
             var=(ccl/fiat_data_last_dict["ccl_gd30"] - 1) * 100),
    ]

    fiat_table = FiatTable(fiat)


    cryptos_data = models.Cryptos.objects.values("data").first()
    cryptos_data_dict = cryptos_data.get("data", {})
    Crypto = namedtuple("Crypto", ["banco", "coin", "compra", "venta", "hora"])

    cryptos = []
    for crypto_dict in cryptos_data_dict:
        for banco, data in crypto_dict.items():
            compra = data["totalAsk"]
            venta = data["totalBid"]
            hora = data["time"]
            coin = "USDT"

            crypto_item = Crypto(
                banco=banco,
                coin=coin,
                venta=compra,
                compra=venta,
                hora=hora
            )
            cryptos.append(crypto_item)

    binance_data = models.Binance.objects.values("data").first()
    binance_data_dict = binance_data.get("data", [])

    binance_dai_item = Crypto(
                    banco='Binance P2P',
                    coin='DAI',
                    compra=None,
                    venta=None,
                    hora=None,
                    )
    
    binance_usdt_item = Crypto(
                banco='Binance P2P',
                coin='USDT',
                compra=None,
                venta=None,
                hora=None,
                )

    for binance_dict in binance_data_dict:
        try:
            data = binance_dict.get("Binance", {})
            coin = data.get("coin", "")
            hora = data.get("time", 0)
            price = float(data.get("price", 0))

            if coin == 'USDT':
                if data["operation"] == 'buy':
                    binance_usdt_item = binance_usdt_item._replace(venta=price, hora=hora)
                else:
                    binance_usdt_item = binance_usdt_item._replace(compra=price)
            elif coin == 'DAI':
                if data["operation"] == 'buy':
                    binance_dai_item = binance_dai_item._replace(venta=price, hora=hora)
                else:
                    binance_dai_item = binance_dai_item._replace(compra=price)

        except models.Binance.DoesNotExist:
            print("Binance data does not exist in the database.")
    
    cryptos.append(binance_usdt_item)
    cryptos.append(binance_dai_item)

    cryptos_table = CryptosTable(cryptos, order_by=request.GET.get("sort"))

    return render(
        request,
        "dolar.html",
        {
            "bancos_table": bancos_table,
            "fiat_table": fiat_table,
            "fiatHora": fiatHora,
            "cryptos_table": cryptos_table,
        },
    )

def home(request):

    fiat_data = models.Fiat.objects.values("data").first()
    fiat_data_last = models.Fiat.objects.values("data_last").first()
    fiat_data_dict = fiat_data.get("data", {})
    fiat_data_last_dict = fiat_data_last.get("data_last", {})
    bancos_data = models.Banco.objects.all().values()
    bna_data = bancos_data[0]["data"]["bna"]
    binance_data = models.Binance.objects.values("data").first()

    try:
        mep = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    except:
        mep = fiat_data_dict["mepgd30"]

    try:
        ccl = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30C", plazo="48hs")[0].ultimo
    except:  
        ccl = fiat_data_dict["cclgd30"]

    var_data = {
        "oficial": (fiat_data_dict["oficial"] / fiat_data_last_dict["oficial"] - 1) * 100,
        "blue": (fiat_data_dict["blue"] / fiat_data_last_dict["blue"] - 1) * 100, 
        "crypto": (float(binance_data["data"][0]["Binance"]["price"]) / float(fiat_data_last_dict["crypto"]) - 1) * 100, 
        "mep": (mep/fiat_data_last_dict["mep_gd30"] - 1) * 100,
        "ccl": (ccl/fiat_data_last_dict["ccl_gd30"] - 1) * 100,
    }

    context = {
        "binance": binance_data, 
        "fiat": fiat_data_dict, 
        "last": fiat_data_last_dict, 
        "bna": bna_data, 
        "mep": mep, 
        "ccl": ccl,
        "var": var_data,
    }

    return render(request, "home.html", context)
